import scrapy
import html2text
import cld2
import dateparser
from datetime import datetime


class PostsSpider(scrapy.Spider):
    linksFile = open('./links/all_italy_links.txt', 'r')

    name = "italy_posts"
    start_urls = map(lambda link: 'http://www.salute.gov.it' + link if link.startswith(
        'http') == False else link, linksFile.read().split(','))

    def parse(self, response):
        now = datetime.utcnow().replace(microsecond=0).isoformat()
        url = response.url
        datetimeToday = now + 'Z'
        contentElement = response.css('.col-md-8').get()
        converter = html2text.HTML2Text()
        converter.ignore_links = True
        date = response.css(
            '.col-md-8 > p > strong::text').getall()[-1].replace('\xa0', ' ')
        updatedDate = dateparser.parse(date, languages=['en', 'it']).date()
        title = response.css('title::text').get()
        text = converter.handle(contentElement)
        isReliable, textBytesFound, details = cld2.detect(text)
        language = details[0].language_name
        yield{
            'title': title,
            'source': 'Testata di proprietà del Ministero della Salute',
            'published': updatedDate,
            'url': url,
            'scraped': datetimeToday,
            'classes': ['Government'],
            'country': 'Italy',
            'municipality': 'National',
            'language': language,
            'text': text
        }
