import scrapy
import html2text
import cld2
from datetime import datetime


class PostsSpider(scrapy.Spider):
    linksFile = open('./links/all_germany_links.txt', 'r')

    name = "germany_posts"
    start_urls = linksFile.read().split(',')

    def parse(self, response):
        now = datetime.utcnow().replace(microsecond=0).isoformat()
        url = response.url
        datetimeToday = now + 'Z'
        contentElement = response.css('.bpa-richtext').get()
        contentElement = response.css('#main').get()  if contentElement is None else contentElement
        converter = html2text.HTML2Text()
        converter.ignore_links = True
        updatedDate = response.css('.bpa-time > time::attr(datetime)').get()
        title = response.css('title::text').get().split(' | ')[-1]
        text = converter.handle(contentElement)
        isReliable, textBytesFound, details = cld2.detect(text)
        language = details[0].language_name
        yield{
            'title': title,
            'source': 'Presse- und Informationsamt der Bundesregierung',
            'published': updatedDate,
            'url': url,
            'scraped': datetimeToday,
            'classes': ['Government'],
            'country': 'Germany',
            'municipality': 'National',
            'language': language,
            'text': text
        }
