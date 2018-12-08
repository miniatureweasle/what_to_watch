# -*- coding: utf-8 -*-
import os
import re
import sys
import django
import scrapy

from pathlib import Path
from core.models import Movie

proj_path = Path(os.path.abspath(__file__)).parents[3]
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "what_to_watch.settings")
sys.path.append(proj_path)
os.chdir(proj_path)
django.setup()

MOVIE_LOOKUPS = {
    'title': "div[@class='lister-item-content']/h3[@class='lister-item-header']/a/text()",
    'rating': "div[@class='lister-item-content']/div[@class='ratings-bar']/div[@class='inline-block ratings-imdb-rating']/strong/text()",
    'release_year': "div[@class='lister-item-content']/h3[@class='lister-item-header']/span[@class='lister-item-year text-muted unbold']/text()",
    'genre': "//span[@class='genre']/text()",
    'votes': "div[@class='lister-item-content']/p[@class='sort-num_votes-visible']/span[2]/text()"
}


class ImdbSpider(scrapy.Spider):
    name = 'imdb'
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/search/title?title_type=feature',]

    def parse(self, response):
        movies = response.xpath("//div[@class='lister-item mode-advanced']")
        for movie in movies:
            title = movie.xpath(MOVIE_LOOKUPS['title']).extract_first()
            rating = movie.xpath(MOVIE_LOOKUPS['rating']).extract_first()
            release_year = movie.xpath(MOVIE_LOOKUPS['release_year']).extract_first()
            genre = movie.xpath(MOVIE_LOOKUPS['genre']).extract_first()
            votes = movie.xpath(MOVIE_LOOKUPS['votes']).extract_first() 

            # prepare for db
            genre = genre.replace('\n', '').strip()
            # if rating can't be found put it at bottom on list
            rating = float(rating) if rating else 0
            print(release_year)
            votes = int(re.sub('[^0-9]','', votes)) if votes else None
            try:
                release_year = int(re.sub('[^0-9]','', release_year)) if release_year else None
            except ValueError:
                release_year = None

            Movie.objects.update_or_create(
                title = title,
                rating = rating,
                release_year = release_year,
                genre = genre,
                votes = votes
            )
            yield {
                'title': title,
                'genre': genre,
                'release_year': release_year,
                'rating': rating,
                'votes': votes
            }

        next_page = response.xpath("//a[@class='lister-page-next next-page']/@href").extract_first()
        if next_page is not None:
            next_page = next_page.replace('&amp;','&')
            url = response.urljoin(next_page)
            yield scrapy.Request(url=url, callback=self.parse)
