import scrapy

filename = 'links/all_spain_links.txt'
class LinksSpider(scrapy.Spider):
    counter = 0
    name = "spain_links"
    start_urls = [
        'https://www.mscbs.gob.es/profesionales/cargarNotas.do?time=1577833200000'
    ]

    def parse(self, response):
        links = response.css('.col-sm-8.col-md-9.informacion > p > a::attr(href)').getall()
        masterLinks = filter(lambda link: link.startswith('cargarNotas.do'),links)
        subLinks = filter(lambda link: link.startswith('cargarNotas.do') == False,links)
        writeToFile(response,list(masterLinks),list(subLinks))
        self.counter+=1
        if self.counter < len(list(masterLinks)):
            print(str(self.counter)+'+'+str(len(links)))
            next_page = response.urljoin(links[self.counter])
            yield scrapy.Request(next_page,callback=self.parse)

def writeToFile(response,links,linksToWrite):
    if response.url == response.urljoin(links[0]):
        open(filename,'w').close()
        with open(filename,'a') as myFile:
            myFile.write(''.join(linksToWrite))
    else:
        with open(filename,'a') as myFile:
            myFile.write(''.join(linksToWrite))
