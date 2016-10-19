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
            'url':'http://tamilyogi.cc/category/tamilyogi-dvdrip-movies/'
        }]

        return [section for section in sections if section['name'] and section['url']]

    def get_movies(self, url):
        movies = [{
            'name': 'Movies1',
            'url': 'http://vidmad.net/embed-9iejdznxifly.html',
        }, {
            'name': 'Movies2',
            'url': 'http://tamilyogi.cc/movie2',
        }]

        return [movie for movie in movies if movie['name'] and movie['url']]