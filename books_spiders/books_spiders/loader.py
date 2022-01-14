from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst

from .items import BooksSpidersItem

class BookItemLoader(ItemLoader):
    default_item_class = BooksSpidersItem
    default_output_processor = TakeFirst()