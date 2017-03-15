from log_files import set_logger
from scrapy.spiders import CrawlSpider
from dateutil.parser import parse
from items import NewsItem
import scrapy
import json
import urlparse

with open("news_json.json", "r") as f:
    scopes = json.load(f)


class NewsSpider(CrawlSpider):
    name = "toi"
    site_name = scopes["toi"]
    start_urls = [site_name["start_urls"]]
    set_logger()

    def parse(self, response):

        for headlines in response.css(self.site_name["url"]).extract():
            yield scrapy.Request(response.urljoin(headlines), callback=self.parse_stories)

    def parse_stories(self, response):
        def extract_with_css(query):
            return "".join(response.css(query).extract()).strip()

        raw_image_1 = response.css(self.site_name["image_1"]).extract_first()
        if raw_image_1 is not None:
            print "****RAW IMAGE-1:", raw_image_1
            if raw_image_1.endswith(".jpg"):
                image = urlparse.urljoin(response.url, raw_image_1)
        else:
            raw_image_2 = response.css(self.site_name["image_2"]).extract_first()
            image = urlparse.urljoin(response.url, raw_image_2)
            print "****RAW IMAGE-2:", raw_image_2

        title = extract_with_css(self.site_name["title_2"])
        pub_date_raw1 = parse(extract_with_css(self.site_name["date"]), fuzzy_with_tokens=True)[0]
        fmt = '%Y-%m-%d %H:%M:%S'
        pub_date = pub_date_raw1.strftime(fmt)
        url = response.url
        story = ""
        raw_story = response.css(self.site_name["story"])
        for texts in raw_story:
            args = (texts.css("::text"). extract(), texts.css("a::text").extract())
            story += "".join(args[0]).strip()

        my_item = NewsItem(title=title, story=story, date=pub_date, file_urls=[image])
        return my_item

