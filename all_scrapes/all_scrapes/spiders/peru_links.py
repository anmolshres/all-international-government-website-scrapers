import scrapy
import re
import math

filename = 'links/all_peru_links.txt'
class LinksSpider(scrapy.Spider):
    counter = 1
    maxPage = 0
    name = "peru_links"
    start_urls = [
        'https://www.gob.pe/busquedas?contenido[]=noticias&desde=01-01-2020&institucion[]=minsa&reason=sheet&sheet=1&term=coronavirus'
    ]

    def parse(self, response):
        allText = response.xpath("//script[contains(., 'window.initialData')]/text()").extract()[0]
        linksToWrite = re.findall(r"href=\\\"(.*?)\\\"",allText)
        if 'sheet=1&' in response.url:
            maxPageString = re.findall(r'"total_count":(.*?),',allText)[0]
            self.maxPage = math.ceil(int(maxPageString) / 25)
        writeToFile(response,linksToWrite,str(self.maxPage))
        self.counter+=1
        if self.counter <= self.maxPage:
            next_page = response.url.replace(f'sheet={self.counter-1}&',f'sheet={self.counter}&')
            yield scrapy.Request(next_page,callback=self.parse)

def writeToFile(response,linksToWrite,pageMax):
    if 'sheet=1&' in response.url:
        open(filename,'w').close()
        with open(filename,'a') as myFile:
            myFile.write(','.join(linksToWrite)+',')
    else:
        with open(filename,'a') as myFile:
            if f'sheet={pageMax}&' in response.url:
                myFile.write(','.join(linksToWrite))
            else:
                myFile.write(','.join(linksToWrite)+',')
