import urllib2
import xbmc
import re

from resources.lib import stream_resolver
from resources.lib import utils
from resources.lib.utils import ADDON_ID, ICON_NEXT, ICON_240, ICON_360, ICON_720

'''
    Main API for thiraimix site
'''

class Thiraimix(object):
    def __init__(self, plugin):
        self.plugin = plugin

    @property
    def get_site_name(self):
        """
        set site name
        :return:
        """
        return 'thiraimix'

    def get_main_url(self):
        """
        site site main url
        :return:
        """
        return 'http://www.thiraimix.com'

    def get_sections(self):
        """
        get all section for tamilyogi website
        :return:
        """
        sections = [
            {
                'name': 'Vijay TV',
                'url': 'http://www.thiraimix.com/channels/vijay-tv',
            },
            {
                'name': 'Sun TV',
                'url': 'http://www.thiraimix.com/channels/sun-tv',
            },
            {
                'name': 'Zee Tamil TV',
                'url': 'http://www.thiraimix.com/channels/zee-tamil',
            },
            {
                'name': 'Color Tamil TV',
                'url': 'http://www.thiraimix.com/channels/colors-tamil',
            },
            {
                'name': 'Polimalar TV',
                'url': 'http://www.thiraimix.com/channels/polimer-tv',
            },
            {
                'name': 'Raj TV',
                'url': 'http://www.thiraimix.com/channels/raj-tv',
            }
        ]
        
        return [section for section in sections if section['name'] and section['url']]

    def get_programmes(self, url):
        """
        get all programme by channel from given section url
        :param url:
        :return:
        """

        items = []

        soup = utils.get_soup_from_url(url)
        for video_colmn in soup.find_all('div', class_='video_colmn'):
            href = video_colmn.find('a')['href']
            if href == None:
                continue

            name = video_colmn.find('img')['alt'] 
            img = video_colmn.find('img')['src'] 
        
            item = dict(name=name, image=img, url=self.get_main_url() + href,
                             infos={'title': name})

            items.append(item)
        
        
        sorted_items = sorted(items, key=lambda k: k['name']) 
        return sorted_items


    def get_episodes(self, url):
        """
        get all episodes from given url
        :param url:
        :return:
        """

        episodes = []

        soup = utils.get_soup_from_url(url)
        for video_colmn_list in soup.find_all('div', class_='video_colmn_list'):
            try:
                href = video_colmn_list.find('a')['href']
            except TypeError:
                continue

            if href == None:
                continue

            name = video_colmn_list.find('a').get_text()
            day = video_colmn_list.find('span', class_='d-ate').get_text()
            month = video_colmn_list.find('span', class_='m-oth').get_text()
            day_letter = video_colmn_list.find('span', class_='d-ayss').get_text()
        
            _name = day + ' ' + month + '  ' + day_letter + ' | ' + name

            episode = dict(name=_name, url=self.get_main_url() + href, prog_name=name, infos={'title': name})

            episodes.append(episode)
        
        return episodes



    def get_stream_urls(self, name, url):
        """
        get stream urls from movie page url.
        :param movie_name:
        :param url:
        :return:
        """
        soup = utils.get_soup_from_url(url)
        stream_urls = []

        video_wrap = soup.find('div', {'class': 'video_wrap'})

        try:
            tamiltvtube = video_wrap.find('iframe', {'src': re.compile(r'http://tamiltvtube.*?')})['src']
            stream_urls = stream_resolver.load_tamiltvtube_videos(tamiltvtube)
        except:
            print ('###### Except tamiltvtube')
            tamiltvtube = None

        
        try:
            youtube = video_wrap.find('iframe', {'src': re.compile(r'https?://.*?youtube.*?')})['src']
            resolved_url = stream_resolver.load_youtube_video(youtube)
            stream_url = {
                'url': resolved_url,
                'quality': 'YouTube',
                'quality_icon': ''
            }
            stream_urls.append(stream_url)

        except:
            print ('###### Except youtube')
            youtube = None


        try:
            dailymotion = video_wrap.find('iframe', {'src': re.compile(r'https?://.*?dailymotion.*?')})['src']
            resolved_url = stream_resolver.load_dailymotion_video(dailymotion)
            print ('##### Dailymotion resolved %s' %resolved_url)
            stream_url = {
                'url': resolved_url,
                'quality': 'Dailymotion',
                'quality_icon': ''
            }
            stream_urls.append(stream_url)
        except:
            print ('###### Except dailymotion')
            dailymotion = None

        print ('#### Stream URL  %s' %stream_urls)

        return [{'name': name,
                 'quality': stream_url['quality'],
                 'quality_icon': stream_url['quality_icon'],
                 'url': stream_url['url']} for stream_url in stream_urls if stream_url['url']]
