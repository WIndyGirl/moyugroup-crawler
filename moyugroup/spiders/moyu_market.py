# -*- coding: utf-8 -*-
from moyugroup.moyu_base import MoyuBaseSpider

class MoyuMarketSpider(MoyuBaseSpider):
    name = 'moyu-market'
    cid = 3
    offset = 0
    count = 2000
    start_urls = ['http://readhubapi.moyugroup.com/readhub/api/v2/collections/detail?cid=%d&offset=%d&count=%d' % (cid, offset, count)]