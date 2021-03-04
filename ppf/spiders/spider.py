import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import PpfItem
from itemloaders.processors import TakeFirst
pattern = r'(\xa0)?'

class PpfSpider(scrapy.Spider):
	name = 'ppf'
	start_urls = ['https://www.ppfbanka.cz/en/press-releases/archive/2?year=#archive']

	def parse(self, response):
		post_links = response.xpath('//td[@class="md-show"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):

		date = response.xpath('//span[@class="date"]/text()').get()
		title = response.xpath('//h1//text()').getall()[2].strip()
		content = response.xpath('//div[@class="col-xl-8 offset-xl-2 col-12"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))


		item = ItemLoader(item=PpfItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
