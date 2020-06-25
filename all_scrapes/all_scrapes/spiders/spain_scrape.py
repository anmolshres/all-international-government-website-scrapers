import scrapy
import html2text
import cld2
import dateparser
from datetime import datetime
from functools import reduce


class PostsSpider(scrapy.Spider):
    linksFile = open('./links/all_spain_links.txt', 'r')

    name = "spain_posts"
    start_urls = map(lambda link: 'https://www.mscbs.gob.es' + link if link.startswith(
        'https') == False else link, linksFile.read().split('..'))

    def parse(self, response):
        now = datetime.utcnow().replace(microsecond=0).isoformat()
        url = response.url
        datetimeToday = now + 'Z'
        converter = html2text.HTML2Text()
        converter.ignore_links = True
        dateArray = response.css(
            '.col-sm-8.col-md-9.informacion > div > p > strong::text').getall()
        dateArrayFiltered = list(filter(lambda current: '2020' in current, dateArray))
        date = dateArrayFiltered[0] if len(dateArrayFiltered) !=0 else None
        if date is None:
            date = response.css('.col-sm-8.col-md-9.informacion > div > p::text').get().split('-')[0]
        if date is not None:
            date = date if len(date.split(',')) == 1 else date.split(',')[1]
            parsedDateTime = dateparser.parse(date, languages=['en', 'es'])
            updatedDate = parsedDateTime.date() if parsedDateTime is not None else 'N/A'
        title = response.css('.col-sm-8.col-md-9.informacion > h2::text').get()
        contentArray = response.css(
            '.col-sm-8.col-md-9.informacion > div').getall()
        text = reduce(lambda first, second: converter.handle(
            first)+converter.handle(second), contentArray)
        isReliable, textBytesFound, details = cld2.detect(text)
        language = details[0].language_name
        yield{
            'title': title,
            'source': 'Ministerio de Sanidad, Consumo y Bienestar Social',
            'published': updatedDate,
            'url': url,
            'scraped': datetimeToday,
            'classes': ['Government'],
            'country': 'Spain',
            'municipality': 'National',
            'language': language,
            'text': text
        }
