import scrapy
import html2text
import cld2
import dateparser
from datetime import datetime


class PostsSpider(scrapy.Spider):
    linksFile = open('./links/vietnam_links.txt', 'r')

    name = "vietnam_posts"
    start_urls = linksFile.read().split(',')

    def parse(self, response):
        now = datetime.utcnow().replace(microsecond=0).isoformat()
        url = response.url
        datetimeToday = now + 'Z'
        contentElement = response.css('#content_detail_news').get()
        contentElement = contentElement if contentElement != None else response.css(
            '.journal-content-article').get()
        converter = html2text.HTML2Text()
        converter.ignore_links = True
        date = response.css('.text-ngayxam-page::text').get()
        updatedDateTime = dateparser.parse(
            date+' +0700', languages=['en', 'vi'])
        updatedDateTimeToPush = str(updatedDateTime).replace(' ', 'T')
        title = response.css(
            '.taglib-header > .header-title > span::text').get().replace('\n', '').replace('\t', '')
        text = converter.handle(contentElement)
        isReliable, textBytesFound, details = cld2.detect(text)
        language = details[0].language_name
        yield{
            'title': title,
            'source': 'BỘ Y TẾ',
            'published': updatedDateTimeToPush,
            'url': url,
            'scraped': datetimeToday,
            'classes': ['Government'],
            'country': 'Viet Nam',
            'municipality': 'National',
            'language': language,
            'text': text
        }
