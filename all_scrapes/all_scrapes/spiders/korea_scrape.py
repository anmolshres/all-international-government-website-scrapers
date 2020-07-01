import scrapy
import html2text
import cld2
import dateparser
from datetime import datetime


class PostsSpider(scrapy.Spider):
    linksFile = open('./links/all_korea_links.txt', 'r')

    name = "korea_posts"
    start_urls = linksFile.read().split(',')

    def parse(self, response):
        now = datetime.utcnow().replace(microsecond=0).isoformat()
        url = response.url
        datetimeToday = now + 'Z'
        contentElement = response.css('.bvc_txt').get()
        detailsElement = response.css('.bvc_detail::text').getall()
        converter = html2text.HTML2Text()
        converter.ignore_links = True
        date = detailsElement[-1]
        updatedDateTime = dateparser.parse(
            date+' +0900', languages=['en', 'ko'])
        updatedDateTimeToPush = str(updatedDateTime).replace(' ', 'T')
        title = response.css('.bv_ttl > h4::text').get()
        text = converter.handle(contentElement)
        isReliable, textBytesFound, details = cld2.detect(text)
        language = details[0].language_name
        source = detailsElement[0]
        yield{
            'title': title,
            'source': source,
            'published': updatedDateTimeToPush,
            'url': url,
            'scraped': datetimeToday,
            'classes': ['Government'],
            'country': 'Korea',
            'municipality': 'National',
            'language': language,
            'text': text
        }
