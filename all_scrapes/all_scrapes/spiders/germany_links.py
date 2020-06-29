import scrapy
import re

filename = 'links/all_germany_links.txt'
class LinksSpider(scrapy.Spider):
    counter = 0
    maxPage = 0
    name = "germany_links"
    start_urls = [
        'https://www.bundesregierung.de/breg-de/suche/992800!search?f=1495774%3A1726012&page=0'
    ]

    def parse(self, response):
        allText = response.xpath("//script[contains(., 'BPA.initialSearchResultsJson')]/text()").extract()[0]
        linksToWrite = [x.group() for x in re.finditer(r'https://www.bundesregierung.de/breg-de/(.*?)\\', allText)]
        maxPageString = re.findall(r'"pageCount":(.*?),', allText)[0]
        if (response.url).endswith('page=0'):
            linksToWrite = filter(lambda link: 'https://www.bundesregierung.de/breg-de/themen/coronavirus\\' != link, linksToWrite)
            self.maxPage = int(maxPageString) - 1
        writeToFile(response,linksToWrite,str(self.maxPage))
        self.counter+=1
        if self.counter <= self.maxPage:
            next_page = response.url[:-1]+str(self.counter) if self.counter <= 10 else response.url[:-2]+str(self.counter)
            yield scrapy.Request(next_page,callback=self.parse)

def writeToFile(response,linksToWrite,pageMax):
    if (response.url).endswith('page=0'):
        open(filename,'w').close()
        with open(filename,'a') as myFile:
            myFile.write(','.join(linksToWrite)+',')
    else:
        with open(filename,'a') as myFile:
            if((response.url).endswith('page='+pageMax)):
                myFile.write(','.join(linksToWrite))
            else:
                myFile.write(','.join(linksToWrite)+',')
