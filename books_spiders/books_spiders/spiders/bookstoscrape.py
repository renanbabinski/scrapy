import scrapy


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
        title = response.xpath('//*[contains(@class, "product_main")]//h1//text()').get()
        thumbnail = response.xpath('//div[@class="carousel-inner"]//div//img//@src').get()
        rate = response.xpath('//*[contains(@class, "product_main")]//p[contains(@class, "star-rating")]//@class').get().split(' ')[-1]
        stock = response.xpath('//*[contains(@class, "product_main")]//p[@class="instock availability"]').re_first(r"(\d+)")
        description = response.xpath('//article[@class="product_page"]/p//text()').get()
        price = response.xpath('//*[contains(@class, "product_main")]//p[@class="price_color"]//text()').get()
        return{
            "title": title,
            "thumbnail": thumbnail,
            "rate": rate,
            "stock": stock,
            "description": description,
            "price": price
        }
