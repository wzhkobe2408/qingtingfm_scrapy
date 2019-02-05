import scrapy
from bs4 import BeautifulSoup
import re
import traceback
from pathlib import Path
import os

from qingtingfm.items import QingtingfmItem

class QingtingfmSpider(scrapy.Spider):

    # name for the spider
    name = 'qingtingfm'
    baseUrl = 'https://www.qingting.fm'

    # start urls
    start_urls = [
        'https://www.qingting.fm/'
    ]

    # custom settings
    custom_settings = {
        'LOG_LEVEL': 'ERROR'
    }

    # parse function
    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        tags = soup.find_all('a', href=re.compile(r"\/channels\/\d*$"))
        for tag in tags:
            # print(tag.text.strip())
            url = self.baseUrl + tag.get('href')
            yield scrapy.Request(url, callback=self.parse_details_and_continue_crawling)

    def parse_details_and_continue_crawling(self, response):
        # 1. Parse details
        soup = BeautifulSoup(response.body, 'html.parser')
        # Get title
        try:
            title = self.extract_title(soup)
            play_count = self.extract_playcount(soup)
            thumb_url = self.extract_thumburl(soup)
            stars = self.extract_stars(soup)
            latest_update = self.extract_latest_update(soup)
            if title is None:
                raise Exception('title not found for ' + response.url)
            if play_count is None:
                raise Exception('play_count not found for ' + response.url)
            if thumb_url is None:
                raise Exception('thumb_url not found for ' + response.url)
            if latest_update is None:
                raise Exception('latest_update not found for ' + response.url)
            if stars is None:
                raise Exception('stars not found for ' + response.url)
            print('==========================')
            print(title)
            item = QingtingfmItem(_id=response.url, title=title, play_count=play_count,
                                  thumb_url=thumb_url, stars=stars, latest_update=latest_update)
            yield item
        except Exception as e:
            self.logger.error(str(e))
            self.logger.error(traceback.format_exc())

        # 2. Continue crawling
        tags = soup.find_all('a', href=re.compile(r"\/channels\/\d*$"))
        for tag in tags:
            # print(tag.text.strip())
            url = self.baseUrl + tag.get('href')
            yield scrapy.Request(url, callback=self.parse_details_and_continue_crawling)

    def extract_title(self, soup):
        selectors = ['h1._3h7q']
        for selector in selectors:
            if len(soup.select(selector)) != 0:
                title = soup.select(selector)[0].text
                return title

    def extract_playcount(self, soup):
        selectors = ['span._8-O6']
        for selector in selectors:
            if len(soup.select(selector)) != 0:
                play_count = soup.select(selector)[0].text
                return play_count

    def extract_thumburl(self, soup):
        selectors = ['div._115e._2p_y > img']
        for selector in selectors:
            if len(soup.select(selector)) != 0:
                thumb_url = soup.select(selector)[0].get('src')
                return thumb_url

    def extract_stars(self, soup):
        selectors = ['span.sprite.sprite-big-fillstar']
        for selector in selectors:
            if len(soup.select(selector)) != 0:
                return len(soup.select(selector))

    def extract_latest_update(self, soup):
        selectors = ['div._2iGm span:nth-child(4)']
        for selector in selectors:
            if len(soup.select(selector)) != 0:
                latest_update = soup.select(selector)[0].text
                return latest_update


