import scrapy
import re
import math

filename = 'links/all_iran_links.txt'
class LinksSpider(scrapy.Spider):
    counter = 1
    maxPage = 0
    name = "iran_links"
    start_urls = [
        'http://irangov.ir/search?page=1&tid=286474&'
    ]

    def parse(self, response):
        if 'page=1&' in response.url:
            maxPageElement = response.css('.resultSearch > .d-box-header.list-news-title > .d-box-title-text::text').get()
            maxPageString = re.findall(r'تعداد یافته ها        (.*?) مورد',maxPageElement)[0]
            self.maxPage = math.ceil(int(maxPageString) / 10)
        linksToWrite = response.css('.news-thumb-link::attr(href)').getall()
        writeToFile(response,linksToWrite,str(self.maxPage))
        self.counter+=1
        if self.counter <= self.maxPage:
            next_page = f'http://irangov.ir/search?page={self.counter}&tid=286474&'
            yield scrapy.Request(next_page,callback=self.parse)

def writeToFile(response,linksToWrite,pageMax):
    if 'page=1&' in response.url:
        open(filename,'w').close()
        with open(filename,'a') as myFile:
            myFile.write(','.join(linksToWrite)+',')
    else:
        with open(filename,'a') as myFile:
            if f'page={pageMax}&' in response.url:
                myFile.write(','.join(linksToWrite))
            else:
                myFile.write(','.join(linksToWrite)+',')
