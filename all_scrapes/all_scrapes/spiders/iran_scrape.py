import scrapy
import html2text
import cld2
import dateparser
from datetime import datetime


class PostsSpider(scrapy.Spider):
    linksFile = open('./links/all_iran_links.txt', 'r')

    name = "iran_posts"
    start_urls = map(lambda link: 'http://irangov.ir' + link if link.startswith(
        'http') == False else link, linksFile.read().split(','))

    def parse(self, response):
        now = datetime.utcnow().replace(microsecond=0).isoformat()
        url = response.url
        datetimeToday = now + 'Z'
        dateElement = response.css('.content_detail_date.col-12::text').get()
        date = dateElement.replace('\r', '').replace(
            '\n', '').replace('  ', '')
        contentElement = response.css('.content_detail_body').get()
        contentElement = response.css('.content_detail').get() if contentElement is None else contentElement
        converter = html2text.HTML2Text()
        converter.ignore_links = True
        updatedDateTime = dateparser.parse(date+' +0430')
        updatedDateTimeToPush = str(updatedDateTime).replace(' ', 'T')
        title = response.css('title::text').get()
        text = converter.handle(contentElement)
        isReliable, textBytesFound, details = cld2.detect(text)
        language = details[0].language_name
        sourceText = response.css(
            '.categorys_list > li > a::text').getall()[-1]
        source = sourceText.replace('\r', '').replace(
            '\n', '').replace('  ', '')
        yield{
            'title': title,
            'source': source,
            'published': updatedDateTimeToPush,
            'url': url,
            'scraped': datetimeToday,
            'classes': ['Government'],
            'country': 'Iran',
            'municipality': 'National',
            'language': language,
            'text': text
        }
