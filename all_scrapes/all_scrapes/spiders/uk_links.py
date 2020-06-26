import scrapy

filename = 'links/all_uk_links.txt'
class LinksSpider(scrapy.Spider):
    counter = 1
    maxPage = 0
    name = "uk_links"
    start_urls = [
        'https://www.gov.uk/search/all?content_purpose_supergroup%5B%5D=news_and_communications&level_one_taxon=5b7b9532-a775-4bd2-a3aa-6ce380184b6c&order=updated-newest&page=1'
    ]

    def parse(self, response):
        maxPageElement = response.css('.gem-c-pagination__link-label::text').get()
        maxPageString = maxPageElement.split(' of ')[1]
        self.maxPage = int(maxPageString)
        links = response.css('.gem-c-document-list__item > a::attr(href)').getall()
        writeToFile(response,links,str(self.maxPage))
        self.counter+=1
        if self.counter <= self.maxPage:
            next_page = response.url[:-1]+str(self.counter) if self.counter <= 10 else response.url[:-2]+str(self.counter)
            yield scrapy.Request(next_page,callback=self.parse)

def writeToFile(response,linksToWrite,pageMax):
    if (response.url).endswith('page=1'):
        open(filename,'w').close()
        with open(filename,'a') as myFile:
            myFile.write(','.join(linksToWrite)+',')
    else:
        with open(filename,'a') as myFile:
            if((response.url).endswith('page='+pageMax)):
                myFile.write(','.join(linksToWrite))
            else:
                myFile.write(','.join(linksToWrite)+',')
