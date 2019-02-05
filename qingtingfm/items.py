# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QingtingfmItem(scrapy.Item):
    # Url of channel detail page
    _id = scrapy.Field()
    title = scrapy.Field()
    play_count = scrapy.Field()
    thumb_url = scrapy.Field()
    stars = scrapy.Field()
    latest_update = scrapy.Field()
