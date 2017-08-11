# -*- coding: utf-8 -*-
import scrapy
import re

class GenericSpider(scrapy.Spider):
    name = 'generic'
    allowed_domains = ['example.com']
    start_urls = ['http://example.com/']

    def __init__(self, domain='', url='', pattern='', *args, **kwargs):
        super(GenericSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url]
        self.allowed_domains = [domain]
        self.pattern = pattern

    def parse(self, response):
        self.logger.info('URL: %s', response.url)
        self.logger.info('pattern: %s', self.pattern)
        for href in response.css('a::attr(href)'):
            if href is not None:
                if re.search(self.pattern, href.extract()):
                    yield response.follow(href, self.parse_item)

    def parse_item(self, response):
        self.logger.info('ITEM URL: %s', response.url)
        yield {
            'title': response.css('title::text').extract_first(),
            'url': response.url,
            'canonical': response.css('link[rel="canonical"]::attr(href)').extract_first(),
            'og_url': response.css('meta[property="og:url"]::attr(content)').extract_first(),
        }
