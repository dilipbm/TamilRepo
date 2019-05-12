import xbmc

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

class TamilRasigan(object):
    def __init__(self, plugin):
        self.plugin = plugin

    @property
    def get_site_name(self):
        """
        set site name
        :return:
        """
        return 'tamilrasigan'

    def get_main_url(self):
        """
        site site main url
        :return:
        """
        return 'http://tamilrasigan.net/'

    def get_sections(self):
        """
        get all section for tamilyogi website
        :return:
        """
        sections = [
            {'name': 'New release',
             'url': 'http://tamilrasigan.net/tamil-movies-online/'},
            {'name': 'Search',
             'url': 'http://tamilrasigan.net/?s='},

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

        if url == 'http://tamilrasigan.net/?s=':
            s = self.plugin.keyboard("", "Search for movie name")
            url += str(s)

        soup = utils.get_soup_from_url(url)

        for movie_list in soup.find_all('ul', class_='lcp_catlist'):
            soup = utils.get_soup_from_text(str(movie_list))
            for m in soup.find_all('a'):
                title = m.get('title')
                url = m.get('href')

                if title is not None:
                    #t = utils.movie_name_resolver(title)
                    #print ('Searchin in OMDB {}'.format(t))
                    #r = omdb.get_movie_info(title=t)
                    #print (r)
                    try:
                        d = dict(name=utils.movie_name_resolver(title), image='', url=url, infos=infos)
                        movies.append(d)
                    except:
                        pass


        if bool(next_page): #If next page
            movies.append(next_page)

        if len(movies) == 0:
            self.plugin.notify(msg="404 No movies found", title='Not found')
        return [movie for movie in movies if movie['name'] and movie['url']]

    def get_stream_urls(self, movie_name, url):
        """
        get stream urls from movie page url.
        :param movie_name:
        :param url:
        :return:
        """
        stream_urls = []
        soup = utils.get_soup_from_url(url)

        l = soup.find_all('iframe')
        for iframe in l:
            src = iframe.get('src')
            link = urllib2.urlparse.urlsplit(src)
            host = link.hostname
            host = host.replace('www.', '')
            host = host.replace('.com', '')

            print ('hostname is ---> ' + host)

            if host.lower() == 'videohost2':
                stream_url = stream_resolver.load_videohost2_video(src)
                print ('Got stream url for videohost2 : {0}'.format(stream_url))
                stream_urls.append(stream_url)

            else:
                print ('Host ingored!!')


        return [{'name': movie_name,
                 'quality': '',
                 'quality_icon': '',
                 'url': stream_url} for stream_url in stream_urls]


