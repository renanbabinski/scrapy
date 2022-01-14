import scrapy
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..loader import BookItemLoader


class BookstoscrapeSpider(CrawlSpider):
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

    pagination_lx = LinkExtractor(
        restrict_xpaths='//ul[@class="pager"]//li[@class="next"]//a'
    )

    rules = [
        Rule(category_lx),
        Rule(pagination_lx),
        Rule(product_lx, callback='parse_book')
    ]

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
        
        
