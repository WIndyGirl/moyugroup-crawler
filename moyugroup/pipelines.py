# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem
import re

class MoyugroupPipeline(object):
    def process_item(self, item, spider):
        file_path = item['original_html_file_path']
        file_name = item['original_html_file_name']
        file_object = open(file_path + file_name, 'r+b')
        try:
            html = file_object.read()
            ## 替换文件url到本地路径
            if item[FilesPipeline.DEFAULT_FILES_RESULT_FIELD]:
                for result in item[FilesPipeline.DEFAULT_FILES_RESULT_FIELD]:
                    html = self.replaceFileUrl(result, html)
            ## 替换image url到本地路径
            if item[ImagesPipeline.DEFAULT_IMAGES_RESULT_FIELD]:
                for result in item[ImagesPipeline.DEFAULT_IMAGES_RESULT_FIELD]:
                    html = self.replaceImgUrl(result, html)
            ## 替换data-src 为src，让图片可以正常显示
            html = html.replace("data-src", "src")

            ## 保存替换后的html到文件
            file_object.seek(0)
            file_object.write(html)
            file_object.truncate()
        finally:  
            file_object.close()
        return item
    def replaceFileUrl(self, result, html):
        url = result['url']
        escaped_url = url.replace("/", "\/").replace("?", "\?")
        pattern = re.compile(escaped_url)
        html = re.sub(pattern, "../files/" + result['path'], html)
        return html
        
    def replaceImgUrl(self, result, html):
        url = result['url']
        escaped_url = url.replace("/", "\/").replace("?", "\?")
        pattern = re.compile(escaped_url)
        html = re.sub(pattern, "../images/" + result['path'], html)
        return html