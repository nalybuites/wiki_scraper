#!/usr/bin/python

import scrapy
from reading_score import ReadingScore
from bs4 import BeautifulSoup

class WikipediaSpider(scrapy.Spider):
    name = 'wikipedia'
    start_urls = ['https://en.wikipedia.org/wiki/Main_Page']
    filtered_list = list(('Wikipedia:', 'Special:', 'Talk:', 'Help:', 'Template:', 'File:'))
    passthrough_list = list(('Portal:', 'Category:'))
    base_host = 'en.wikipedia.org'
    visited = set()

    def parse(self, response):
        return self.parse_internal(response)

    def parse_internal(self, response):
        local_queue = set()

        for href in response.css('a::attr("href")'):
            full_url = response.urljoin(href.extract())

            # ignore these pages
            if any(sub in full_url for sub in self.filtered_list):
                continue
            
            # not within the same language
            if self.base_host not in full_url:
                continue

            # must be part of the wiki
            if '/wiki/' not in full_url:
                continue

            # already crawled
            if full_url in self.visited:
                continue

            local_queue.add(full_url)

        for url in local_queue:
            # pass through pages
            if any(sub in url for sub in self.passthrough_list):
                yield scrapy.Request(url, callback=self.passthrough)
                continue

            yield scrapy.Request(url, callback=self.parse_text)

    def passthrough(self, response):
        self.visited.add(response.url)
        return self.parse_internal(response)

    def parse_text(self, response):
        self.visited.add(response.url)
        soup = BeautifulSoup(response.body, 'html.parser')
        rs = ReadingScore()
        x = rs.get_all(soup.get_text())
        print x
        return self.parse_internal(response)

    def closed(self, reason):
        print reason
        print self.visited
