# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksSpidersItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    thumbnail = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    rate = scrapy.Field()
    stock = scrapy.Field()
