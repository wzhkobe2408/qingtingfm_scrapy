import scrapy
from bs4 import BeautifulSoup
import re


class QingtingfmSpider(scrapy.Spider):

    # name for the spider
    name = "qingtingfm"

    # start urls
    start_urls = [
        "https://www.qingting.fm/"
    ]

    # parse function
    def parse(self, response):
        soup = BeautifulSoup(response.body, "html.parser")
        tags = soup.find_all('a', href=re.compile(r"\/channels\/.*"))
        for tag in tags:
            print(tag.text.strip())
