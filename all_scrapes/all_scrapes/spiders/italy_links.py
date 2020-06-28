import scrapy

filename = 'links/all_italy_links.txt'
class LinksSpider(scrapy.Spider):
    counter = 0
    maxPage = 0
    name = "italy_links"
    start_urls = [
        'http://www.salute.gov.it/portale/nuovocoronavirus/archivioNotizieNuovoCoronavirus.jsp?lingua=italiano&menu=notizie&p=dalministero&area=nuovocoronavirus&notizie.page=0'
    ]

    def parse(self, response):
        maxPageElement = response.css('.paginazione > p::text').get()
        maxPageString = maxPageElement.split('\xa0')[-1]
        self.maxPage = int(maxPageString) - 1
        links = response.css('.col-md-8 > div > dl > dt > a::attr(href)').getall()
        writeToFile(response,links,str(self.maxPage))
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
