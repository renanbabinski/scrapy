import scrapy
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from ..loader import BookItemLoader


class BookstoscrapeSpider(scrapy.Spider):
    name = 'bookstoscrape'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    category_lx = LinkExtractor(
        allow=r'catalogue/category',
        restrict_xpaths='//ul[@class="nav nav-list"]//a'
    )

    product_lx = LinkExtractor(
        allow=r'catalogue/[\w\-_]+/index.html',
        restrict_xpaths='//article[@class="product_pod"]//h3'
    )

    def parse(self, response):
        for link in self.category_lx.extract_links(response):
            yield scrapy.Request(response.urljoin(link.url),
                                 callback=self.parse_category)

    def parse_category(self, response):
        for link in self.product_lx.extract_links(response):
            yield scrapy.Request(response.urljoin(link.url),
                                 callback=self.parse_book)

    def parse_book(self, response):
        loader = BookItemLoader(response=response)

        loader.add_xpath('title', '//*[contains(@class, "product_main")]//h1//text()')
        loader.add_xpath('thumbnail', '//div[@class="carousel-inner"]//div//img//@src')
        loader.add_xpath('description', '//article[@class="product_page"]/p//text()')
        loader.add_xpath('price', '//*[contains(@class, "product_main")]//p[@class="price_color"]//text()')
        
        rate_xpath = '//*[contains(@class, "product_main")]//p[contains(@class, "star-rating")]//@class'
        loader.add_value('rate', response.xpath(rate_xpath).get().split(' ')[-1])

        stock_xpath = '//*[contains(@class, "product_main")]//p[@class="instock availability"]'
        loader.add_value('stock', response.xpath(stock_xpath).re_first(r"(\d+)"))

        return loader.load_item()
        
        
