# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2
import urlparse
import os
import logging
from datetime import datetime
from scrapy.exceptions import DropItem
import re


class NewsPipeline(object):

    fmt = '%Y-%m-%d %H:%M:%S'
    creation_date_raw = datetime.now()
    creation_date = creation_date_raw.strftime(fmt)

    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["DATABASE_URL"])

    def __init__(self):
        self.conn = psycopg2.connect(database=self.url.path[1:], user=self.url.username,password=self.url.password, host=self.url.hostname, port=self.url.port)

    def process_item(self, item, spider):

        if not item["date"]:
            item["date"] = self.creation_date
            logging.warning("****Article Does Not Contain any Date****")
            logging.info("****Adding Date****")
            return item

        if not item["title"]:
            raise DropItem("****Missing title in %s****" % item)

        check_for_duplicates = self.check_dupes(item)

        if check_for_duplicates:
            logging.info("**********Duplicate Article**********")
            logging.info("Skipping . . . . .")
            return item
        else:
            clean_story = self.strip_story(item["story"])
            item["story"] = clean_story
            clean_image = self.strip_images(item["files"][0]["path"])
            item["files"][0]["path"] = clean_image
            save_item = self.save_to_database(item)
            return save_item

    def check_dupes(self, item):
        cur = self.conn.cursor()
        cur.execute("SELECT count(*) FROM blog_post WHERE title=%s", (item["title"],))
        fetch_id = cur.fetchone()[0]
        return fetch_id

    def save_to_database(self, item):
        cur = self.conn.cursor()
        cur.execute("""
                    INSERT INTO blog_post (title,text,creation_date,image_name,author_id) VALUES (%s,%s,%s,%s,%s)""",
                    (item["title"], item["story"], item["date"], item["files"][0]["path"], 1))
        logging.info("*" * 50)
        logging.info("***Found a New Article***")
        logging.info("**Saving to Database**")
        self.conn.commit()
        return item

    @staticmethod
    def strip_story(story):
        raw_story = " ".join(story.strip().split())
        stripped_story = re.sub(r"(.+?\.)\s(.+?)", r"\1\n\2", raw_story)
        return stripped_story

    @staticmethod
    def strip_images(images):
        if not images.endswith(".jpg"):
            logging.warning("*****Article Image Not in JPG Format*****")
            logging.info("*****Removing Image*****")
            images = None
            return images
        else:
            image_name = images.split("/")[1]
            return image_name
