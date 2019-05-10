import helper
import urllib2
import stream_resolver
import xbmc

'''
    Main API for tamilyogi site
'''

addon_id = 'plugin.video.tamilstreamer'
icon_next = xbmc.translatePath('special://home/addons/{0}/resources/images/next.png'.format(addon_id))


#icon_next = 'https://raw.githubusercontent.com/dilipbm/TamilRepo/master/plugin.video.tamilstreamer/resources/images/next.png'
#icon_720 = 'https://raw.githubusercontent.com/dilipbm/TamilRepo/master/plugin.video.tamilstreamer/resources/images/icon_720.png'
#icon_360 = 'https://raw.githubusercontent.com/dilipbm/TamilRepo/master/plugin.video.tamilstreamer/resources/images/icon_360.png'
#icon_240 = 'https://raw.githubusercontent.com/dilipbm/TamilRepo/master/plugin.video.tamilstreamer/resources/images/icon_240.png'

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
        return 'http://tamilyogi.cc/'

    def get_sections(self):
        """
        get all section for tamilyogi website
        :return:
        """
        sections = [{   'name': 'Tamil New Movies',
                        'url': 'http://tamilyogi.cc/category/tamilyogi-full-movie-online/',},
                    {'name': 'Tamil Bluray Movies',
                    'url': 'http://tamilyogi.cc/category/tamilyogi-bluray-movies/',},
                    {'name': 'Tamil DVDRip Movies',
                     'url': 'http://tamilyogi.cc/category/tamilyogi-dvdrip-movies/'},
                    {'name': 'Tamil Dubbed Movies',
                     'url': 'http://tamilyogi.cc/category/tamilyogi-dubbed-movies-online/'},
                    {'name': 'Search',
                     'url': 'http://tamilyogi.cc/?s='}
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

        if url == 'http://tamilyogi.cc/?s=':
            s = self.plugin.keyboard("", "Search for movie name")
            url += str(s)

        soup = helper.get_soup_from_url(url)

        for a in soup.find_all('a'):
            title = a.get('title')
            try:
                nextpagetag = a.get('class')
                if 'next' in nextpagetag:
                    next_page_url = a.get('href')
                    next_page = {'name': 'Next Page',
                                 'image': icon_next,
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
                        d = dict(name=helper.movie_name_resolver(title), image=img, url=a.get('href'),
                                 infos={'title': helper.movie_name_resolver(title)})
                        movies.append(d)
                        added_items.append(title)
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
                #print(src)
                stream_urls = stream_resolver.load_fastplay_video(src)

            elif host.lower() == 'vidorg':
                stream_urls = stream_resolver.load_vidorg_videos(src)

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
