# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MoyugroupItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    original_html_file_name = scrapy.Field()
    original_html_file_path = scrapy.Field()
