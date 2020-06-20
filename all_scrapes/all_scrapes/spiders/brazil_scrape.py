import scrapy
import html2text
import cld2
import dateparser
from datetime import datetime
from functools import reduce


class PostsSpider(scrapy.Spider):
    linksFile = open('./links/all_brazil_links.txt', 'r')

    name = "brazil_posts"
    start_urls = map(lambda link: 'https://www.saude.gov.br' + link if link.startswith(
        'https') == False else link, linksFile.read().split(','))

    def parse(self, response):
        now = datetime.utcnow().replace(microsecond=0).isoformat()
        url = response.url
        datetimeToday = now + 'Z'
        textContent = 'todo'
        dateElement = response.css('span.documentModified::text').get()
        dateElementText = dateElement.replace('\t', '').replace('\n', '')
        dateElementArray = dateElementText.split(',')
        updatedDateISO = dateparser.parse(
            dateElementArray[1], languages=['en', 'pt']).date()
        updatedTimeISO = dateElementArray[2][1:].replace('h', ':')+'-03:00'
        updatedDateTime = str(updatedDateISO)+'T'+updatedTimeISO
        title = response.css('title::text').get()
        contentArray = response.css('.item-page > p').extract()
        contentArray = response.css('.item-pagenoticias > p').extract() if len(contentArray) == 0 else contentArray
        contentArray = response.css('.item-page::text').extract() if len(contentArray) == 0 else contentArray
        converter = html2text.HTML2Text()
        converter.ignore_links = True
        text = reduce(lambda first, second: converter.handle(
            first)+converter.handle(second), contentArray)
        isReliable, textBytesFound, details = cld2.detect(text)
        language = details[0].language_name
        yield{
            'title': title,
            'source': 'Agência Saúde',
            'published': updatedDateTime,
            'url': url,
            'scraped': datetimeToday,
            'classes': ['Government'],
            'country': 'Brazil',
            'municipality': 'National',
            'language': language,
            'text': text
        }
