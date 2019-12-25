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

class Tamildbox(object):
    def __init__(self, plugin):
        self.plugin = plugin

    @property
    def get_site_name(self):
        """
        set site name
        :return:
        """
        return 'tamildbox'

    def get_main_url(self):
        """
        site site main url
        :return:
        """
        return 'http://www.tamildbox.world'

    def get_sections(self):
        """
        get all section for tamilyogi website
        :return:
        """
        sections = [
            {
                'name': 'Tamil Movies',
                'url': 'http://www.tamildbox.world/movies',
            },
            {
                'name': 'TV Series',
                'url': 'http://www.tamildbox.top/tv-series'
            },
            {
                'name': 'Search',
                'url': 'http://www.tamildbox.world/filter'
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

        if url == 'http://www.tamildbox.world/filter':
            s = xbmcgui.Dialog().input("Search for movie name")
            if s == '':
                return []

            url = 'http://www.tamildbox.world/filter?name={}&submit='.format(s)

        soup = utils.get_soup_from_url(url)
        for listbox in soup.find_all('div', class_='listbox'):
            try:
                title = listbox.find('div', class_='name').text
            except:
                continue
 
            try:
                quality_name = listbox.find('span', class_='overlay').text.strip().rstrip()

            except:
                quality_name = ''

            try:
                img = listbox.find('img')['src'].strip()
                
            except:
                img = ''

            try:
                onclick = listbox.find('div', class_='play')['onclick']
                url = re.findall(r"'(http.*?)'", onclick)[0]
            except:
                continue

            try:
                next_page_url = soup.find('div', class_='pagination').find_all('a')[-1]['href']
                next_page = {'name': 'Next Page',
                             'image': ICON_NEXT,
                             'infos':{},
                             'url': next_page_url}
            except:
                pass

            try:
                if title not in added_items:
                    d = dict(name=utils.movie_name_resolver(title) + ' ' + quality_name, image=img, url=url,
                             infos={'title': utils.movie_name_resolver(title)})
                    movies.append(d)
                    added_items.append(title)
            except:
                pass

        if bool(next_page): #If next page
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
        # http://www.tamildbox.world/actions.php?case=loadEP&ep_id=1st&server_id=1577
        # siteURL+'actions.php?case=loadEP&ep_id='+escape(ep_id)+'&server_id='+escape(server_id);

        items = []
        stream_urls = []
        soup = utils.get_soup_from_url(url)

        #loadEP = re.findall(r"loadEP\((.*?)\)", soup.text)[0].split(',')
        for loadEP in re.findall(r"loadEP\((.*?)\)", soup.text):
            loadEP = loadEP.split(',')
            ep_id = loadEP[0].replace("'","").rstrip()
            server_id = loadEP[1].replace("'","").rstrip()
            _action_url = 'http://www.tamildbox.world/actions.php?case=loadEP&ep_id={}&server_id={}'.format(ep_id,server_id)
            print('####### Action URL: {}'.format(_action_url))
            soup = utils.get_soup_from_url(_action_url)

            # Grab embadded links
            embeded_urls = [item.get('src') for item in soup.find_all('iframe')]
        
            print('##### embaded {}'.format(embeded_urls))

            for emb_url in embeded_urls:
                if 'ssfiles' in emb_url:
                    resolved = stream_resolver.resolve_ssfiles(emb_url)
                    items += [{
                        'name': movie_name,
                        'quality': item['quality'],
                        'quality_icon': item['quality_icon'],
                        'url': item['url']
                    } for item in resolved]

                elif 'dailymotion' in emb_url:
                    resolved = stream_resolver.load_dailymotion_video(emb_url)

                    items += [{
                        'name': movie_name,
                        'quality': 'Dailymotion',
                        'quality_icon': '',
                        'url': resolved
                    }]             

                else:
                    print('Host {} not found in resolver'.format(emb_url))

        return items
