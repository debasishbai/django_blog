from log_files import set_logger
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider
from items import NewsItem
import scrapy
import json
import urlparse
import re

with open("news_json.json", "r") as f:
    scopes = json.load(f)


class NewsSpider(scrapy.Spider):
    name = "toi"
    site_name = scopes["ndtv"]
    start_urls = [site_name["start_urls"]]
    allowed_domains = site_name["allowed_domains"]
    set_logger()

    def parse(self, response):

        for move_to_story in response.css(self.site_name["response_css"]):
            page_to_scrape = move_to_story.css(self.site_name["url"]).extract_first()
            filter_links = re.match(r".*//.*?/(\w+)", page_to_scrape).groups()[0]
            if filter_links in self.site_name["deny"]:
                continue
            yield scrapy.Request(move_to_story.css(self.site_name["url"]).extract_first(), callback=self.parse_stories)

        next_page = response.css(self.site_name["page"]).extract()
        for number in range(len(next_page[:-1])):
            # print "Page No: ", next_page[number]
            yield scrapy.Request(next_page[number], callback=self.parse)

    def parse_stories(self, response):
        print "Reached: ", response.url
        # if response.url.startswith("http://gadgets.ndtv.com"):
        matched = re.match(r".*//(\w+).*", response.url).groups()[0]
        item = dict()
        dept = {"www": self.www, "gadgets": self.gadgets, "profit": self.profit, "sports": self.sports}
        details = dept[matched](item, response)
        print details
        title = details.get("title")
        image = details.get("image")
        caption = details.get("caption", None)
        story = details.get("story")

        my_item = NewsItem(title=title, story=story, caption=caption, image_urls=[image])
        return my_item

    def www(self, item, response):
        item['title'] = response.css(self.site_name["ndtv_title"]).extract_first()
        image_scopes = self.site_name["ndtv_image"].values()
        item['image'] = self.search(response, image_scopes)
        caption_scopes = self.site_name["ndtv_caption"].values()
        item['caption'] = self.search(response, caption_scopes)
        raw_story = response.css(self.site_name["ndtv_story"])
        item["story"] = self.strip_story(raw_story)
        return item

    def gadgets(self, item, response):
        title_scopes = self.site_name["gadgets_title"].values()
        item['title'] = self.search(response, title_scopes)
        image_scopes = self.site_name["gadgets_image"].values()
        item["image"] = self.search(response, image_scopes)
        raw_story = response.css(self.site_name["gadgets_story"])
        item["story"] = self.strip_story(raw_story)
        return item

    def profit(self, item, response):
        item['title'] = response.css(self.site_name["profit_title"]).extract_first()
        item["image"] = response.css(self.site_name["profit_image"]).extract_first()
        item["caption"] = response.css(self.site_name["profit_caption"]).extract_first()
        raw_story = response.css(self.site_name["profit_story"])
        item["story"] = re.sub(r"(.*)\s{4}!function.*1\);(.*)", r"\1\2", self.strip_story(raw_story))
        return item

    def sports(self, item, response):
        item["title"] = response.css(self.site_name["sports_title"]).extract_first()
        item["image"] = response.css(self.site_name["sports_image"]).extract_first()
        item["caption"] = response.css(self.site_name["sports_caption"]).extract_first()
        raw_story = response.css(self.site_name["sports_story"])
        item["story"] = self.strip_story(raw_story)
        return item

    @staticmethod
    def strip_story(raw_story):
        story = ""
        for text in raw_story:
            args = (text.css("::text").extract(), text.css("a::text").extract())
            story += "".join(args[0])
        return story

    @staticmethod
    def search(response, scopes):
        count = 0
        while count < len(scopes):
            data = response.css(scopes[count]).extract_first()
            count += 1
            if data is not None:
                break
        return data


# process = CrawlerProcess()
# process.crawl(NewsSpider)
# process.start()
