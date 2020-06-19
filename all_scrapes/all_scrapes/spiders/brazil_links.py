import scrapy
import os


class LinksSpider(scrapy.Spider):
    name = "brazil_links"

    start_urls = [
        'https://www.saude.gov.br/noticias?filter-search=coronavirus&limit=0&filter-start_date=&filter-end_date=&filter_order=&filter_order_Dir=&limitstart=&task='
    ]

    def parse(self, response):
        links = response.css(
            'div.span9.tileContent > h2 > a::attr(href)').getall()
        linksAfter2019 = filter(
            lambda link: '/noticias/svs/15676-instituto-evandro-chagas-completa-78-anos-e-novo-diretor-toma-posse' not in link, links)
        os.chdir('./links/')
        filename = 'all_brazil_links.txt'
        with open(filename, 'w') as f:
            f.write(','.join(linksAfter2019))
        os.chdir('..')
