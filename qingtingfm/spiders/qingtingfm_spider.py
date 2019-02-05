import scrapy
from bs4 import BeautifulSoup
import re


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
        tags = soup.find_all('a', href=re.compile(r"\/channels\/.*"))
        for tag in tags:
            # print(tag.text.strip())
            url = self.baseUrl + tag.get('href')
            yield scrapy.Request(url, callback=self.parse_details)

    def parse_details(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        # Get title
        try:
            title = self.extract_title(soup)
            playcount = self.extract_playcount(soup)
            thumburl = self.extract_thumburl(soup)
            starts = self.extract_stars(soup)
            latestupdate = self.extract_latest_update(soup)
            if title is None:
                raise Exception('title not found for ' + response.url)
            if playcount is None:
                raise Exception('playcount not found for ' + response.url)
            if thumburl is None:
                raise Exception('thumburl not found for ' + response.url)
            if latestupdate is None:
                raise Exception('latestupdate not found for ' + response.url)
            if starts is None:
                raise Exception('stars not found for ' + response.url)
            print('==========================')
            print(title)
            print(playcount)
            print(thumburl)
            print(float(starts))
            print(latestupdate)
        except Exception as e:
            self.logger.error(str(e))

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
                playcount = soup.select(selector)[0].text
                return playcount

    def extract_thumburl(self, soup):
        selectors = ['div._115e._2p_y > img']
        for selector in selectors:
            if len(soup.select(selector)) != 0:
                thumburl = soup.select(selector)[0].get('src')
                return thumburl

    def extract_stars(self, soup):
        selectors = ['span.sprite.sprite-big-fillstar']
        for selector in selectors:
            if len(soup.select(selector)) != 0:
                return len(soup.select(selector))

    def extract_latest_update(self, soup):
        selectors = ['div._2iGm span:nth-child(4)']
        for selector in selectors:
            if len(soup.select(selector)) != 0:
                latestupdate = soup.select(selector)[0].text
                return latestupdate


