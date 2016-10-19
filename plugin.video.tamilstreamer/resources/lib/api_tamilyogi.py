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
        movies, nexte_page_url = tamilyogi_scraper.movie_loader(section_url)
        print type(movies)
        pprint.pprint(movies)
        #       movies = [{
        #          'name': 'Movies1',
        #         'url': 'http://vidmad.net/embed-9iejdznxifly.html',
        #     }, {
        #         'name': 'Movies2',
        #           'url': 'http://tamilyogi.cc/movie2',
        #       }]

        return [movie for movie in movies if movie['name'] and movie['url']]

    def get_stream_urls(self, movie_name, movie_url):
        stream_urls = [{
            'name': movie_name,
            'quality': '720',
            'url': 'http://cdn26.vidmad.net/h7todndpamlbu3tf6rutl6xm3ge7fojx5ul3x547refqoa5lldlrhpet2xdq/v.mp4',
        }, {
            'name': movie_name,
            'quality': '360',
            'url': 'http://cdn26.vidmad.net/h7todndpamlbu3tf6rutl6xm3ge7fojx5ul3x547refqoa5lldlrhpet2xdq/v.mp4',
        }
        ]

        return [stream_url for stream_url in stream_urls if stream_url['name'] and stream_url['url']]
