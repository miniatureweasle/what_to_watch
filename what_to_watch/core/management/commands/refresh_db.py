from django.core.management.base import BaseCommand

import scrapy
from scrapy.crawler import CrawlerProcess

from core.scrapers.imdb import ImdbSpider


def spider_closing(spider):
    """Activates on spider closed signal"""
    reactor.stop()



class Command(BaseCommand):

    def handle(self, *args, **options):
        
        process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })
        process.crawl(ImdbSpider)
        process.start()

