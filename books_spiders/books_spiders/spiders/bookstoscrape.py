import scrapy
from scrapy.loader import ItemLoader
from books_spiders.books_spiders.items import BooksSpidersItem


class BookstoscrapeSpider(scrapy.Spider):
    name = 'bookstoscrape'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        for path in response.xpath('//ul[@class="nav nav-list"]//a//@href').getall():
            yield scrapy.Request(response.urljoin(path),
                                 callback=self.parse_category)

    def parse_category(self, response):
        for path in response.xpath('//article[@class="product_pod"]//h3//@href').getall():
            yield scrapy.Request(response.urljoin(path),
                                 callback=self.parse_book)

    def parse_book(self, response):
        loader = ItemLoader(BooksSpidersItem(), response=response)

        loader.add_xpath('title', '//*[contains(@class, "product_main")]//h1//text()')
        loader.add_xpath('thumnail', '//div[@class="carousel-inner"]//div//img//@src')
        loader.add_xpath('description', '//*[contains(@class, "product_main")]//p[contains(@class, "star-rating")]//@class')
        loader.add_xpath('price', '//*[contains(@class, "product_main")]//p[@class="instock availability"]')
        rate = 


        loader.add_xpath('', '//article[@class="product_page"]/p//text()')
        loader.add_xpath('', '//*[contains(@class, "product_main")]//p[@class="price_color"]//text()')
        
