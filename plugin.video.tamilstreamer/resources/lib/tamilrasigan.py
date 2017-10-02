import helper
import urllib2
import stream_resolver
from xbmcswift2 import xbmc


'''
    Main API for tamilyogi site
'''

addon_id = 'plugin.video.tamilstreamer'
icon_next = xbmc.translatePath('special://home/addons/{0}/resources/images/next.png'.format(addon_id))

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

        soup = helper.get_soup_from_url(url)

        for movie_list in soup.find_all('ul', class_='lcp_catlist'):
            soup = helper.get_soup_from_text(str(movie_list))
            for m in soup.find_all('a'):
                title = m.get('title')
                url = m.get('href')

                if title is not None:
                    try:
                        d = dict(name=helper.movie_name_resolver(title), image='', url=url, infos={})
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
        stream_urls = None
        soup = helper.get_soup_from_url(url)
        l = soup.find_all('iframe')
        for iframe in l:
            print 'in get_Stream_url'


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

            print 'hostname is ---> ' + host

            if host.lower() == 'vidmad':
                stream_urls = stream_resolver.load_vidmad_video(src)

            elif host.lower() == 'fastplay':
                stream_urls = stream_resolver.load_fastplay_video(src)

            else:
                print 'Host ingored!!'


                # stream_urls = [{
                #     'name': movie_name,
                #     'quality': 'HD',
                #     'url': steam_url
                # }]

        return [{'name': movie_name,
                 'quality': stream_url['quality'],
                 'quality_icon': stream_url['quality_icon'],
                 'url': stream_url['url']} for stream_url in stream_urls if stream_url['url']]


