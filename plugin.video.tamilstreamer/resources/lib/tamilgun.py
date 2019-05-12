import re

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from resources.lib import stream_resolver
from resources.lib import utils
from resources.lib.utils import ADDON_ID, ICON_NEXT, ICON_240, ICON_360, ICON_720

'''
    Main API for tamilyogi site
'''


class Tamilgun(object):
    def __init__(self, plugin):
        self.plugin = plugin

    @property
    def get_site_name(self):
        """
        set site name
        :return:
        """
        return 'tamilgun'

    def get_main_url(self):
        """
        site site main url
        :return:
        """
        return 'http://tamilgun.watch/'

    def get_sections(self):
        """
        get all section for tamilyogi website
        :return:
        """
        sections = [
            {
                'name': 'Tamil HD Movies',
                'url': 'http://tamilgun.watch/categories/hd-movies/',
            }
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

        soup = utils.get_soup_from_url(url)
        for article in soup.find_all('article'):
            try:
                title = article.find('h3').find('a')['title']
            except:
                continue

            try:
                next_page_url = soup.find('a', class_='next')['href']
                next_page = {'name': 'Next Page',
                             'image': ICON_NEXT,
                             'infos':{},
                             'url': next_page_url}
            except:
                pass

            try:
                img = article.find('img')['src'].strip()
                
            except:
                continue

            try:
                if title not in added_items:
                    d = dict(name=utils.movie_name_resolver(title), image=img, url=article.find('h3').find('a')['href'],
                             infos={'title': utils.movie_name_resolver(title)})
                    movies.append(d)
                    added_items.append(title)
            except:
                pass
        if bool(next_page): #If next page
            movies.append(next_page)

        #if len(movies) == 0:
        #    xbmcgui.Dialog().notification(heading='Error 404', message='No movies found')

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

        # Grab .hls links
        hls_streams = [item['src'] for item in soup.find_all('iframe', {'src': re.compile(r'.*?/hls.*?')})]
        if len(hls_streams) > 0:
            for src in hls_streams:
                url = re.sub('/(hls_\w*)/', '/hls/', src) + '/playlist.m3u8'
                p = urlparse(url, 'http')
                stream_urls.append(p.geturl())

        
        items += [{'name': movie_name,
                 'quality': '720',
                 'quality_icon': ICON_720,
                 'url': stream_url} for stream_url in stream_urls]

        # Grab embadded links
        embeded_urls = [item['src'] for item in soup.find_all('iframe', {'src': re.compile(r'(http.*?.html)')})]
        
        for emb_url in embeded_urls:
            if 'ssfiles' in emb_url:
                resolved = stream_resolver.resolve_ssfiles(emb_url)
                items += [{
                    'name': movie_name,
                    'quality': item['quality'],
                    'quality_icon': item['quality_icon'],
                    'url': item['url']
                } for item in resolved]

        return items
