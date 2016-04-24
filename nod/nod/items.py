from scrapy.item import Item, Field


class Notice(Item):
    ad_id = Field()
    url = Field()
    heading = Field()
    body = Field()
    publication_name = Field()
    publication_dates = Field()
