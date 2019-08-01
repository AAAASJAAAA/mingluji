# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MinglujiItem(scrapy.Item):
    # define the fields for your item here like:
    province = scrapy.Field()
    corporate_name = scrapy.Field()
    address = scrapy.Field()
    id_code = scrapy.Field()
    region = scrapy.Field()
    registration_date = scrapy.Field()
    business_scope = scrapy.Field()
    legal_representative = scrapy.Field()
    registered_funds = scrapy.Field()
    corporate_type = scrapy.Field()
    # url = scrapy.Field()
    pass