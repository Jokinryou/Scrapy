# -*- coding: utf-8 -*-

from scrapy.http import Response
import chardet

class Encode():
    """encode to utf-8"""

    def __init__(self):
        pass

    def encode(self, response):
        encoding = chardet.detect(response.body)['encoding']
        if encoding != 'utf-8':
            response.body = response.body.decode(encoding,'replace').encode('utf-8')
