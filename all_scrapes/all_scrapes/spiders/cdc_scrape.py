import scrapy
import html2text
import cld2
import dateparser
from datetime import datetime


class PostsSpider(scrapy.Spider):
    linksFile = open('./links/all_cdc_links.txt', 'r')

    name = "cdc_posts"
    start_urls = map(lambda link: 'https://www.cdc.gov' + link if link.startswith(
        'https') == False else link, linksFile.read().split(','))

    def parse(self, response):
        now = datetime.utcnow().replace(microsecond=0).isoformat()
        url = response.url
        datetimeToday = now + 'Z'
        syndicateContent = response.css('.syndicate').extract()[1] if len(response.css(
            '.syndicate').extract()) > 1 else response.css('.syndicate').extract()[0]
        converter = html2text.HTML2Text()
        converter.ignore_links = True
        date = response.css('span#last-reviewed-date::text').get() if '/travel/notices/warning/coronavirus-cruise-ship' not in url else response.css(
            '.last-reviewed.col > div:nth-of-type(1) > span::text').get()
        updatedDate = dateparser.parse(date, languages=['en', 'es']).date()
        title = response.css('title::text').get() 
        text = converter.handle(syndicateContent)
        isReliable, textBytesFound, details = cld2.detect(text)
        language = details[0].language_name
        yield{
            'title': title,
            'source': 'Centers for Disease Control and Prevention',
            'date': updatedDate,
            'url': url,
            'scraped': datetimeToday,
            'classes': ['Government'],
            'country': 'United States of America',
            'municipality': 'National',
            'language': language,
            'text': text
        }
