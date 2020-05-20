import xbmc
import xbmcgui
import re

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from resources.lib import stream_resolver
from resources.lib import utils
from resources.lib.utils import ADDON_ID, ICON_NEXT, ICON_240, ICON_360, ICON_720

'''
    Main API for tamildbox site
'''


class Tamilarasan(object):
    def __init__(self, plugin):
        self.plugin = plugin

    @property
    def get_site_name(self):
        """
        set site name
        :return:
        """
        return 'tamilarasan'

    def get_main_url(self):
        """
        site site main url
        :return:
        """
        return 'https://tamilarasan.net/'

    def get_sections(self):
        """
        get all section for tamilyogi website
        :return:
        """
        sections = [
            {
                'name': 'New Tamil Movies',
                'url': 'https://tamilarasan.net/watch-new-tamil-movies/new-tamil-movies-tamilgun/',
            },
            {
                'name': 'Tamil HD Movies',
                'url': 'https://tamilarasan.net/watch-new-tamil-movies/tamil-hd-movies/',
            },
            {
                'name': 'New Telugu Movies',
                'url': 'https://tamilarasan.top/new-telugu-movies/',
            },
            {
                'name': 'New Telugu Movies',
                'url': 'https://tamilarasan.top/telugu-hd-movies/',
            },
            {
                'name': 'Tamil Dubbed Movies',
                'url': 'https://tamilarasan.top/tamil-dubbed-movies/',
            }  # ,
            # {
            #    'name': 'Search',
            #    'url': 'https://tamilarasan.net/search',
            # }
        ]

        return [section for section in sections if section['name'] and section['url']]

    def get_movies(self, url):
        """
        get all movies from given section url
        :param url:
        :return:
        """
        movies = []
        added_items = []
        img = ''
        next_page = {}
        infos = {}

        if url == 'https://tamilarasan.net/search':
            s = xbmcgui.Dialog().input("Search for movie name")
            if s == '':
                return []

            url = 'https://tamilarasan.net/?s={}'.format(s)

        soup = utils.get_soup_from_url(url)

        for item in soup.find_all('div', class_='layer-wrapper'):
            try:
                title = item.find('div', class_='layer-content').text
            except:
                continue

            try:
                img = item.find('img')['src'].strip()

            except:
                img = ''

            try:
                url = item.find(
                    'div', class_='layer-content').find('a').get('href')

            except:
                continue

            try:
                next_page_url = soup.find(
                    'a', class_='next page-numbers').get('href')
                next_page = {'name': 'Next Page',
                             'image': ICON_NEXT,
                             'infos': {},
                             'url': next_page_url}
            except:
                pass

            try:
                if title not in added_items:
                    d = dict(name=utils.movie_name_resolver(title), image=img, url=url,
                             infos={'title': utils.movie_name_resolver(title)})
                    movies.append(d)
                    added_items.append(title)
            except:
                pass

        if bool(next_page):  # If next page
            movies.append(next_page)

        if len(movies) == 0:
            xbmcgui.Dialog().notification(heading='Error 404', message='No movies found')

        return [movie for movie in movies if movie['name'] and movie['url']]

    def get_stream_urls(self, movie_name, url):
        """
        get stream urls from movie page url.
        :param movie_name:
        :param url:
        :return:
        """

        items = []
        stream_urls = []
        soup = utils.get_soup_from_url(url)

        # Grab embadded links
        embeded_urls = [item['src'] for item in soup.find_all(
            'iframe', {'src': re.compile(r'(http.*?)')})]

        for emb_url in embeded_urls:
            if 'tamilarasanmovie.com' in emb_url:
                resolved = stream_resolver.resolve_tamilarasanmovie(emb_url)
                items += [{
                    'name': movie_name,
                    'quality': item['quality'],
                    'quality_icon': item['quality_icon'],
                    'url': item['url']
                } for item in resolved]

            elif 'fastplay' in emb_url:
                resolved = stream_resolver.load_fastplay_video(emb_url)
                items += [{
                    'name': movie_name,
                    'quality': item['quality'],
                    'quality_icon': item['quality_icon'],
                    'url': item['url']
                } for item in resolved]

        return items
