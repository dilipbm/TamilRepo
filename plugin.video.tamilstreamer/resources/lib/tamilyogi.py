import xbmc
import xbmcgui

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

from resources.lib import stream_resolver
from resources.lib import utils
from resources.lib.utils import ADDON_ID, ICON_NEXT, ICON_240, ICON_360, ICON_720

'''
    Main API for tamilyogi site
'''


class TamilYogi(object):
    def __init__(self, plugin):
        self.plugin = plugin

    @property
    def get_site_name(self):
        """
        set site name
        :return:
        """
        return 'tamilyogi'

    def get_main_url(self):
        """
        site site main url
        :return:
        """
        return 'http://tamilyogi.vip/'

    def get_sections(self):
        """
        get all section for tamilyogi website
        :return:
        """
        sections = [{   'name': 'Tamil New Movies',
                        'url': 'http://tamilyogi.vip/category/tamilyogi-full-movie-online/',},
                    {'name': 'Tamil Bluray Movies',
                    'url': 'http://tamilyogi.vip/category/tamilyogi-bluray-movies/',},
                    {'name': 'Tamil DVDRip Movies',
                     'url': 'http://tamilyogi.vip/category/tamilyogi-dvdrip-movies/'},
                    {'name': 'Tamil Dubbed Movies',
                     'url': 'http://tamilyogi.vip/category/tamilyogi-dubbed-movies-online/'},
                    {'name': 'Search',
                     'url': 'http://tamilyogi.vip/search'}
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

        if url == 'http://tamilyogi.vip/search':
            s = xbmcgui.Dialog().input("Search for movie name", type=xbmcgui.INPUT_ALPHANUM)
            if s == '':
                return []
            
            url = 'http://tamilyogi.vip/?s={}'.format(s)
            
        soup = utils.get_soup_from_url(url)

        for a in soup.find_all('a'):
            title = a.get('title')
            try:
                nextpagetag = a.get('class')
                if 'next' in nextpagetag:
                    next_page_url = a.get('href')
                    next_page = {'name': 'Next Page',
                                 'image': ICON_NEXT,
                                 'infos':{},
                                 'url': next_page_url}
            except:
                pass

            try:
                img = a.find('img')['src']
            except:
                pass

            if (title is not None) and (title != 'Tamil Movie Online') and img != '':
                try:
                    if title not in added_items:
                        d = dict(name=utils.movie_name_resolver(title), image=img, url=a.get('href'),
                                 infos={'title': utils.movie_name_resolver(title)})
                        movies.append(d)
                        added_items.append(title)
                except:
                    pass
        if bool(next_page): #If next page
            movies.append(next_page)

        #if len(movies) == 0:
        #    self.plugin.notify(msg="404 No movies found", title='Not found')

        return [movie for movie in movies if movie['name'] and movie['url']]

    def get_stream_urls(self, movie_name, url):
        """
        get stream urls from movie page url.
        :param movie_name:
        :param url:
        :return:
        """
        stream_urls = None
        soup = utils.get_soup_from_url(url)
        l = soup.find_all('iframe')
        for iframe in l:

            src = iframe.get('src')
            link = urllib2.urlparse.urlsplit(src)
            host = link.hostname
            host = host.replace('www.', '')
            host = host.replace('.com', '')
            host = host.replace('.tv', '')
            host = host.replace('.net', '')
            host = host.replace('.cc', '')
            host = host.replace('.sx', '')
            host = host.replace('.to', '')

            print ('hostname is ---> ' + host)

            if host.lower() == 'vidmad':
                stream_urls = stream_resolver.load_vidmad_video(src)

            elif host.lower() == 'fastplay':
                #print(src)
                stream_urls = stream_resolver.load_fastplay_video(src)

            elif host.lower() == 'vidorg':
                stream_urls = stream_resolver.load_vidorg_videos(src)

            else:
                print ('Host ingored!!')


                # stream_urls = [{
                #     'name': movie_name,
                #     'quality': 'HD',
                #     'url': steam_url
                # }]

        return [{'name': movie_name,
                 'quality': stream_url['quality'],
                 'quality_icon': stream_url['quality_icon'],
                 'url': stream_url['url']} for stream_url in stream_urls if stream_url['url']]
