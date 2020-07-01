import scrapy
import re
import math

filename = 'links/all_korea_links.txt'


class LinksSpider(scrapy.Spider):
    counter = 1
    maxPage = 0
    name = "korea_links"
    start_urls = [
        'http://ncov.mohw.go.kr/tcmBoardList.do?pageIndex=1&brdId=&brdGubun=&board_id=&search_item=1&search_content='
    ]

    def parse(self, response):
        maxPageString = response.css('.bt_count > strong::text').get()
        elementsWithLinks = response.css('.bl_link').getall()
        linksInfoArray = list(map(lambda link: '|'.join(re.findall(r'onclick="fn_tcm_boardView\((.*?)\);', link)[0].split(',')), elementsWithLinks))
        links = list(map(lambda link: link.replace("'","").replace(' ',''),linksInfoArray))
        
        if 'pageIndex=1&' in response.url:
            self.maxPage = math.ceil(int(maxPageString)/10)
        writeToFile(response, links, str(self.maxPage))
        self.counter += 1
        if self.counter <= self.maxPage:
            next_page = f'http://ncov.mohw.go.kr/tcmBoardList.do?pageIndex={self.counter}&brdId=&brdGubun=&board_id=&search_item=1&search_content='
            yield scrapy.Request(next_page, callback=self.parse)


def writeToFile(response, linksToWrite, pageMax):
    if 'pageIndex=1&' in response.url:
        open(filename, 'w').close()
        with open(filename, 'a') as myFile:
            myFile.write(','.join(linksToWrite)+',')
    else:
        with open(filename, 'a') as myFile:
            if f'pageIndex={pageMax}&' in response.url:
                myFile.write(','.join(linksToWrite))
            else:
                myFile.write(','.join(linksToWrite)+',')
