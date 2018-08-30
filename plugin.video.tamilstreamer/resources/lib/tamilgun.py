import helper
import urllib2
import stream_resolver
from xbmcswift2 import xbmc
import re

'''
    Main API for tamilyogi site
'''

addon_id = 'plugin.video.tamilstreamer'
icon_next = xbmc.translatePath('special://home/addons/{0}/resources/images/next.png'.format(addon_id))
icon_720 = xbmc.translatePath('special://home/addons/{0}/resources/images/icon_720.png'.format(addon_id))
icon_360 = xbmc.translatePath('special://home/addons/{0}/resources/images/icon_360.png'.format(addon_id))
icon_240 = xbmc.translatePath('special://home/addons/{0}/resources/images/icon_240.png'.format(addon_id))

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

        soup = helper.get_soup_from_url(url)

        for article in soup.find_all('article'):
            try:
                title = article.find('h3').find('a')['title']
            except:
                continue

            try:
                next_page_url = soup.find('a', class_='next')['href']
                next_page = {'name': 'Next Page',
                             'image': icon_next,
                             'infos':{},
                             'url': next_page_url}
            except:
                pass

            try:
                img = article.find('img')['src'].strip()
                print (img)
            except:
                continue

            try:
                if title not in added_items:
                    d = dict(name=helper.movie_name_resolver(title), image=img, url=article.find('h3').find('a')['href'],
                             infos={'title': helper.movie_name_resolver(title)})
                    movies.append(d)
                    added_items.append(title)
            except:
                pass
        if bool(next_page): #If next page
            movies.append(next_page)

        if len(movies) == 0:
            self.plugin.notify(msg="404 No movies found", title='Not found')

        print(movies)

        return [movie for movie in movies if movie['name'] and movie['url']]


    def get_stream_urls(self, movie_name, url):
        """
        get stream urls from movie page url.
        :param movie_name:
        :param url:
        :return:
        """
        stream_urls = []
        soup = helper.get_soup_from_url(url)
        hls_streams = [item['src'] for item in soup.find_all('iframe', {'src': re.compile(r'.*?/hls.*?')})]
        
        if len(hls_streams) > 0:
            for src in hls_streams:
                url = re.sub('/(hls_\w*)/', '/hls/', src) + '/playlist.m3u8'
                stream_urls.append(url)
        
        else:
            return []

        return [{'name': movie_name,
                 'quality': '720',
                 'quality_icon': icon_720,
                 'url': stream_url} for stream_url in stream_urls]
