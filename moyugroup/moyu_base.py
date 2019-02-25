
# -*- coding: utf-8 -*-
import scrapy
import json
import os
import re
from moyugroup.items import MoyugroupItem

class MoyuBaseSpider(scrapy.Spider):
    save_dir = "/Users/apple/Person/documents/moyugroup/"
    allowed_domains = ['readhubapi.moyugroup.com', 'mp.weixin.qq.com', 'mmbiz.qpic.cn']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_page_infos)

    def parse_page_infos(self, response):
        jsonresponse = json.loads(response.body_as_unicode())
        data = jsonresponse['data']
        for info in data:
            print info['url']
            yield scrapy.Request(url=info['url'], callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        ## 获取页面可下载链接
        urls = self.getUrl(response.body)

        filename = response.css('h2.rich_media_title::text').get().strip() + ".html"
        with open(self.save_dir + self.name + "/" + filename, 'wb') as f:
            f.write(response.body)
           
        image_urls = []
        file_urls = []
        for item in urls:
            ## 只下载以https开头的链接指向的文件或者图片
            if (not item.startswith("https")):
                continue
            if item.endswith("jpg") or item.endswith("jpeg") or item.endswith("png") or item.endswith("gif"):
                image_urls.append(item)
            else:
                file_urls.append(item)

        mediaItem = MoyugroupItem()
        mediaItem['image_urls'] = image_urls
        mediaItem['file_urls'] = file_urls
        ## file/images下载完以后，需要替换为本地路径，所以需要提供原始html文件路径
        mediaItem['original_html_file_name'] = filename
        mediaItem['original_html_file_path'] = self.save_dir + self.name + "/"
        yield mediaItem

    def getUrl(self, html): 
        patternjs = '<script.*?src="(.*?)"' 
        patternimg = '<img.*?src="(.*?)"' 
        patterncss = '<link.*?href="(.*?)"' 
        patternimg2 = '<div.*?data-src="(.*?)"' 

        href = re.compile(patternjs, re.S | re.I ).findall(html) 
        href += re.compile(patternimg, re.S | re.I).findall(html) 
        href += re.compile(patterncss, re.S | re.I).findall(html) 
        href += re.compile(patternimg2, re.S | re.I).findall(html) 
        return href
        