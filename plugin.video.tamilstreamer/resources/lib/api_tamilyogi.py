from ..scrapers import tamilyogi_scraper

import pprint

'''
    API for tamil yogi
'''


class TamilYogi(object):
    def __init__(self):
        pass

    def get_main_url(self):
        return 'http://tamilyogi.cc/'

    def get_sections(self):
        sections = [{
            'name': 'Tamil New Movies',
            'url': 'http://tamilyogi.cc/category/tamilyogi-full-movie-online/',
        }, {
            'name': 'Tamil Bluray Movies',
            'url': 'http://tamilyogi.cc/category/tamilyogi-bluray-movies/',
        }, {
            'name': 'Tamil DVDRip Movies',
            'url': 'http://tamilyogi.cc/category/tamilyogi-dvdrip-movies/'
        }]

        return [section for section in sections if section['name'] and section['url']]

    def get_movies(self, section_url):
        movies = tamilyogi_scraper.movie_loader(section_url)

        items = [movie for movie in movies if movie['name'] and movie['url']]
        return items

    def get_stream_urls(self, movie_name, movie_url):
        stream_url = tamilyogi_scraper.get_stream_url(movie_url)

        stream_urls = [{
            'name': movie_name,
            'quality': 'HD',
            'url': stream_url
        }]
        return [stream_url for stream_url in stream_urls if stream_url['name'] and stream_url['url']]
