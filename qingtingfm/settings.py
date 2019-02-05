# -*- coding: utf-8 -*-

# Scrapy settings for qingtingfm project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'qingtingfm'

SPIDER_MODULES = ['qingtingfm.spiders']
NEWSPIDER_MODULE = 'qingtingfm.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'qingtingfm (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# MongoDB pipeline
ITEM_PIPELINES = {
    "qingtingfm.pipelines.QingtingfmPipeline": 300,
}

MONGO_HOST = 'localhost'
MONGO_PORT = '27017'
MONGO_DATABASE = 'QINGTING_FM'
