import xbmc
import xbmcgui
import re

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

from resources.lib import stream_resolver
from resources.lib import utils
from resources.lib.utils import ADDON_ID, ICON_NEXT, ICON_240, ICON_360, ICON_720

'''
    Main API for tamildhool site
'''


class TamilDhool(object):
    def __init__(self, plugin):
        self.plugin = plugin

    @property
    def get_site_name(self):
        """
        set site name
        :return:
        """
        return 'tamildhool'

    def get_main_url(self):
        """
        site site main url
        :return:
        """
        return 'https://www.tamildhool.net/'

    def get_sections(self):
        """
        get all section for tamilyogi website
        :return:
        """
        sections = [
            {
                'name': 'Zee Tamil',
                'url': 'https://www.tamildhool.net/zee-tamil-programs/',
            },
            {
                'name': 'Sun TV',
                'url': 'https://www.tamildhool.net/sun-tv-programs/',
            },
            {
                'name': 'Vijay TV',
                'url': 'https://www.tamildhool.net/vijay-tv-programs/',
            },

        ]

        return [section for section in sections if section['name'] and section['url']]

    def get_programmes(self, url):
        """
        get all programme by channel from given section url
        :param url:
        :return:
        """

        print('######## LOAD programmes')
        print('URL: {}'.format(url))

        items = []

        soup = utils.get_soup_from_url(url)
        for item in soup.find_all('div', {'class': 'gallery-item'}):
            img = ''

            try:
                title = item.text.strip()
            except KeyError:
                title = None

            # next_page = {'name': 'Next Page',
            #             'image': ICON_NEXT,
            #             'infos': {},
            #             'url': next_page_url}

            try:
                img_ = item.find_all('img')[0]
            except KeyError:
                img_ = None

            if img_ is not None:
                src = img_.get('src')
                if src is not None:
                    src = img_.get('src')
                    img = src
                else:
                    try:
                        srcset = img_.get('srcset')
                        img = srcset.split(',')[0].split(' ')[0]
                    except KeyError:
                        pass

            try:
                div_ = item.find_all('a')[0]
                link = div_.get('href')
            except KeyError:
                link = None

            if title is not None and link is not None:
                item = dict(name=title, image=img, url=link,
                            infos={'title': title})

            items.append(item)

        sorted_items = sorted(items, key=lambda k: k['name'])
        return sorted_items

    def get_episodes(self, url):
        """
        get all episodes from given url
        :param url:
        :return:
        """

        print('########## episodes')
        print('URL : {}'.format(url))

        episodes = []

        soup = utils.get_soup_from_url(url)
        for item in soup.find_all('article'):
            try:
                href = item.find('a')['href']
            except TypeError:
                continue

            if href == None:
                continue

            name = item.text.strip()
            #day = video_colmn_list.find('span', class_='d-ate').get_text()
            #month = video_colmn_list.find('span', class_='m-oth').get_text()
            # day_letter = video_colmn_list.find(
            #    'span', class_='d-ayss').get_text()

            #_name = day + ' ' + month + '  ' + day_letter + ' | ' + name

            episode = dict(name=name, url=href, prog_name=name,
                           infos={'title': name})

            episodes.append(episode)

        return episodes

    def get_movies(self, url):
        """
        get all movies from given section url
        :param url:
        :return:
        """
        movies = []
        added_items = []
        next_page = {}
        infos = {}

        # if url == 'http://tamilyogi.vip/search':
        #    s = xbmcgui.Dialog().input("Search for movie name", type=xbmcgui.INPUT_ALPHANUM)
        #    if s == '':
        #        return []
        #
        #    url = 'http://tamilyogi.vip/?s={}'.format(s)

        soup = utils.get_soup_from_url(url)

        for item in soup.find_all('div', {'class': 'gallery-item'}):
            img = ''

            try:
                title = item.text.strip()
            except KeyError:
                title = None

            # next_page = {'name': 'Next Page',
            #             'image': ICON_NEXT,
            #             'infos': {},
            #             'url': next_page_url}

            try:
                img_ = item.find_all('img')[0]
            except KeyError:
                img_ = None

            if img_ is not None:
                src = img_.get('src')
                if src is not None:
                    src = img_.get('src')
                    img = src
                else:
                    try:
                        srcset = img_.get('srcset')
                        img = srcset.split(',')[0].split(' ')[0]
                    except KeyError:
                        pass

            try:
                div_ = item.find_all('a')[0]
                link = div_.get('href')
            except KeyError:
                link = None

            if title is not None and link is not None:
                try:
                    if title not in added_items:
                        d = dict(name=utils.movie_name_resolver(title), image=img, url=link,
                                 infos={'title': utils.movie_name_resolver(title)})
                        movies.append(d)
                        added_items.append(title)
                except:
                    pass

        if bool(next_page):  # If next page
            movies.append(next_page)

        # if len(movies) == 0:
        #    self.plugin.notify(msg="404 No movies found", title='Not found')

        return [movie for movie in movies if movie['name'] and movie['url']]

    def get_stream_urls(self, movie_name, url):
        """
        get stream urls from movie page url.
        :param movie_name:
        :param url:
        :return:
        """

        print('########## get stream url')
        print('URL: {}'.format(url))

        stream_urls = []
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

            print('hostname is ---> ' + host)

            if host.lower() == 'vidmad':
                stream_urls = stream_resolver.load_vidmad_video(src)

            elif host.lower() == 'fastplay':
                # print(src)
                stream_urls = stream_resolver.load_fastplay_video(src)

            elif host.lower() == 'vidorg':
                stream_urls = stream_resolver.load_vidorg_videos(src)

            elif host.lower() == 'malarmoon':
                stream_urls = stream_resolver.load_malarmoon_videos(src)

            elif host.lower() == 'tamilbliss':
                stream_urls = stream_resolver.load_tamilbliss_videos(src)

            else:
                print('Host ingored!!')

            try:
                youtube = soup.find(
                    'iframe', {'src': re.compile(r'https?://.*?youtube.*?')})['src']
                resolved_url = stream_resolver.load_youtube_video(youtube)
                stream_url = {
                    'url': resolved_url,
                    'quality': 'YouTube',
                    'quality_icon': ''
                }
                stream_urls.append(stream_url)

            except Exception as e:
                print('###### Except youtube')
                print(e)
                youtube = None

            try:
                dailymotion = soup.find(
                    'iframe', {'src': re.compile(r'https?://.*?dailymotion.*?')})['src']
                resolved_url = stream_resolver.load_dailymotion_video(
                    dailymotion)
                print('##### Dailymotion resolved %s' % resolved_url)
                stream_url = {
                    'url': resolved_url,
                    'quality': 'Dailymotion',
                    'quality_icon': ''
                }
                stream_urls.append(stream_url)
            except:
                print('###### Except dailymotion')
                dailymotion = None

            # stream_urls = [{
            #     'name': movie_name,
            #     'quality': 'HD',
            #     'url': steam_url
            # }]

        print('######### Stream URLS')
        print(stream_urls)

        return [{'name': movie_name,
                 'quality': stream_url['quality'],
                 'quality_icon': stream_url['quality_icon'],
                 'url': stream_url['url']} for stream_url in stream_urls if stream_url['url']]
