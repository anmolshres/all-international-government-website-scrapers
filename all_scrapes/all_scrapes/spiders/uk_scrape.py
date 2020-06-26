import scrapy
import html2text
import cld2
import dateparser
from datetime import datetime


class PostsSpider(scrapy.Spider):
    linksFile = open('./links/all_uk_links.txt', 'r')

    name = "uk_posts"
    start_urls = map(lambda link: 'https://www.gov.uk' + link if link.startswith(
        'https') == False else link, linksFile.read().split(','))

    def parse(self, response):
        now = datetime.utcnow().replace(microsecond=0).isoformat()
        url = response.url
        datetimeToday = now + 'Z'
        contentElement = response.css('.govspeak').get() if response.css('.govspeak').get(
        ) is not None else response.css('.gem-c-govspeak.govuk-govspeak.direction-ltr').get()
        converter = html2text.HTML2Text()
        converter.ignore_links = True
        date = response.css('.app-c-published-dates::text').get().replace('\n',
                                                                          '').replace('Published ', '').replace('  ', '')
        updatedDate = dateparser.parse(date).date()
        title = response.css(
            '.gem-c-title__text.gem-c-title__text--long::text').get().replace('\n', '').replace('  ', '')
        text = converter.handle(contentElement)
        isReliable, textBytesFound, details = cld2.detect(text)
        language = details[0].language_name
        source = response.css(
            '.app-c-publisher-metadata__definition-sentence > a::text').get()
        yield{
            'title': title,
            'source': source,
            'published': updatedDate,
            'url': url,
            'scraped': datetimeToday,
            'classes': ['Government'],
            'country': 'The United Kingdom of Great Britain and Northern Ireland',
            'municipality': 'National',
            'language': language,
            'text': text
        }
