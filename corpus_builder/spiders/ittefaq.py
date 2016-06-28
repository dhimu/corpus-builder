# -*- coding: utf-8 -*-
import scrapy
import dateutil.parser
import datetime
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from corpus_builder.items import TextEntry

# Note: The spider only works for the "Printed Edition", for now.


class IttefaqSpider(CrawlSpider):
    name = "ittefaq"
    allowed_domains = ["ittefaq.com.bd"]

    rules = (
    	Rule(
    		LinkExtractor(
                # http://www.ittefaq.com.bd/national/2016/06/28/74396.html
    			allow=('\/\d{4}\/\d{2}\/\d{2}\/\d+.html$')
    		),
    		callback='parse_news'),
    )
    
    def __init__(self, start_date=None, end_date=None, *a, **kw):
    	self.start_date = dateutil.parser.parse(start_date)
    	self.end_date = dateutil.parser.parse(end_date)

        self.categories = ['first-page', 'last-page', 'city', 'country',
        'world-news', 'entertainment', 'sports-news', 'it-corner', 'trade',
        'editorial', 'sub-editorial', 'drishtikon', 'aiojon', 'aunoshilon',
        'others', 'taronner-shomokalin-chinta']

    	super(IttefaqSpider, self).__init__(*a, **kw)

    def start_requests(self):
    	date_processing = self.start_date
    	while date_processing <= self.end_date:
            for category in self.categories:
                # http://www.ittefaq.com.bd/print-edition/country/2016/06/29
        		url = 'http://www.ittefaq.com.bd/print-edition/{0}/{1}'.format(
                    category,
        			date_processing.strftime('%Y/%m/%d')
        		)
        		yield self.make_requests_from_url(url)
            date_processing += datetime.timedelta(days=1)

    def parse_news(self, response):
    	item = TextEntry()
    	item['body'] = "".join(part for part in response.css('div.details *::text').extract())
    	return item
        
