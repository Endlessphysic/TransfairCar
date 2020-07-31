# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
# Extracted Data temporary saved
import scrapy


class CrawlwithscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    price = scrapy.Field()
    start = scrapy.Field()
    destination = scrapy.Field()
