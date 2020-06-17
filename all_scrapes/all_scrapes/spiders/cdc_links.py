import scrapy
import os

class LinksSpider(scrapy.Spider):
    name = "cdc_links"

    start_urls = [
        'https://www.cdc.gov/coronavirus/2019-ncov/whats-new-all.html'
    ]

    def parse(self, response):
        links = response.css('.list-bullet.feed-item-list > li > a::attr(href)').getall()
        linksWithoutIndex = filter(lambda link: 'coronavirus/2019-ncov/index.html' not in link,links)
        os.chdir('./links/')
        filename = 'all_cdc_links.txt'
        with open(filename,'w') as f:
            f.write(','.join(linksWithoutIndex))
        os.chdir('..')