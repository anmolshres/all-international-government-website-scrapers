import scrapy
import html2text
import cld2
import dateparser
from datetime import datetime


class PostsSpider(scrapy.Spider):
    linksFile = open('./links/all_peru_links.txt', 'r')

    name = "peru_posts"
    start_urls = map(lambda link: 'https://www.gob.pe' + link if link.startswith(
        'http') == False else link, linksFile.read().split(','))

    def parse(self, response):
        now = datetime.utcnow().replace(microsecond=0).isoformat()
        url = response.url
        datetimeToday = now + 'Z'
        contentElement = response.css('.description.institution-document__description').get()
        converter = html2text.HTML2Text()
        converter.ignore_links = True
        date = response.css('.header.institution-document__header.black > p::text').get().split(' - ')[0]
        date = response.css('.header.institution-document__header.black > p::text').getall()[-1].split(' - ')[0] if '2020' not in date else date
        updatedDate = dateparser.parse(date, languages=['en', 'es']).date()
        title = response.css('title::text').get().split(' | ')[0]
        text = converter.handle(contentElement)
        isReliable, textBytesFound, details = cld2.detect(text)
        language = details[0].language_name
        source = response.css('.text-xl.font-normal > a::text').get()
        yield{
            'title': title,
            'source': source,
            'published': updatedDate,
            'url': url,
            'scraped': datetimeToday,
            'classes': ['Government'],
            'country': 'Peru',
            'municipality': 'National',
            'language': language,
            'text': text
        }
