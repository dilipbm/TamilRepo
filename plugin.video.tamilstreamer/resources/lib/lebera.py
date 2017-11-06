import helper
import urllib2
import stream_resolver
from xbmcswift2 import xbmc
from datetime import datetime, timedelta
import requests
import threading, time, uuid
from bs4 import BeautifulSoup

'''
    Main API for lebera site
'''

addon_id = 'plugin.video.tamilstreamer'
icon_next = xbmc.translatePath('special://home/addons/{0}/resources/images/next.png'.format(addon_id))

LOCALE = 'en_GB'
TIMEZONE = '7200'
CLIENT_ID = 'spbtv-web'
CLIENT_VERSION = '0.1.0'
TIMEOFFSET = 5400


class Lebera(object):
    def __init__(self, plugin):
        self.plugin = plugin
        self.storage = plugin.get_storage('lebera_storage', TTL=1440)
        self.storage_deviceinfo = plugin.get_storage('lebera_device', TTL=None)

        self.device_id, self.device_registered = self._get_deviceinfo()
        #print (plugin.list_storages())

        #print (self.storage.keys())
        #self.storage.clear()
        #print (self.storage.keys())
        if 'access_token' in self.storage.keys():
            self.access_token = self.storage['access_token']
        #self.access_token = self._login()


    def _get_deviceinfo(self):

        if 'device_id' in self.storage_deviceinfo.keys():
            print ('Device ID : {}'.format(self.storage_deviceinfo['device_id']))
            device_id = self.storage_deviceinfo['device_id']
            try:
                device_registered = self.storage_deviceinfo['registered']
            except KeyError:
                self.storage_deviceinfo['registered'] = False
                device_registered = False

        else:
            device_id = uuid.uuid4()
            print('Device ID not found. Creating new device ID : {}'.format(device_id))
            self.storage_deviceinfo['device_id'] = str(device_id)
            self.storage_deviceinfo['registered'] = False
            device_registered = False

        return device_id, device_registered

    def manage_connexion(self):

        if hasattr(self, 'access_token'):
            if not self.is_valide_token():
                self._logout(self.access_token)
                self._login()
        else:
            self._login()


    def is_valide_token(self):
        if 'access_token' in self.storage.keys():
            r = self._get_user(self.storage['access_token'])
            if r['meta']['status'] == 200:
                return True
            elif r['meta']['status'] == 401:
                return False


    def _login(self):
        # Verifi if access_token already in local storage
        #storage = self.plugin.get_storage('lebera_storage', TTL=1440)

        #self.storage.pop('access_token')

        print ('Login process start')

        if 'access_token' in self.storage.keys():
            self._logout(self.storage['access_token'])


        headers = {
                'Origin': 'http://play.lebara.com',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json',
                'Referer': 'http://play.lebara.com/fr/en/Tamil/',
                'Connection': 'keep-alive',
            }
        url = 'http://api.lebaraplay.com/api/oauth/token'
        username = self.plugin.get_setting('username', unicode)
        password = self.plugin.get_setting('password', unicode)

        if username == '' or password == '':
            print ('Please enter username and password in addons settings')
            self.plugin.notify('Please enter username and password in addons settings')

        data = [
                ('client_id', CLIENT_ID),
                ('client_version', CLIENT_VERSION),
                ('locale', LOCALE),
                ('timezone', TIMEZONE),
                ('username', username),
                ('password', password),
                ('grant_type', 'password'),
            ]

        r = requests.post(url, headers=headers, data=data)
        if r.status_code != 200:
            print('Erreur lebera login!!!')
            self.plugin.notify('Lebera login failure!!')

        access_token = r.json()['access_token']
        print ('access token {}'.format(access_token))

        if access_token:
            self.storage['access_token'] = access_token
            self.access_token = access_token


    def _logout(self, access_token):
        """A FAIREEEEE"""
        headers = {
            'Origin': 'http://play.lebara.com',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'Referer': 'http://play.lebara.com/fr/en/Tamil/',
            'Connection': 'keep-alive',
        }
        url = 'http://api.lebaraplay.com/api/oauth/token'
        print ('access token to logout {}'.format(access_token))
        data = [
            ('client_id', CLIENT_ID),
            ('client_version', CLIENT_VERSION),
            ('locale', LOCALE),
            ('timezone', TIMEZONE),
            ('access_token', access_token),
        ]

        r = requests.delete(url, headers=headers, data=data)
        if r.status_code == 200:
            print ('Logout success')
            self.storage.pop('access_token')
            print(self.storage.items())

        else:
            print ('Error logout')


    def _get_user(self, access_token):

        headers = {
            'Origin': 'http://play.lebara.com',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'Referer': 'http://play.lebara.com/fr/en/Tamil/',
            'Connection': 'keep-alive',
        }

        params = (
            ('client_id', CLIENT_ID),
            ('client_version', CLIENT_VERSION),
            ('locale', LOCALE),
            ('timezone', TIMEZONE),
            ('access_token', access_token),
        )

        url = 'http://api.lebaraplay.com/api/v1/user'
        r = requests.get(url, headers=headers, params=params)
        try:
            res = r.json()
        except:
            res = None

        return res

    def _register_device(self):

        headers = {
                'Origin': 'http://play.lebara.com',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json',
                'Referer': 'http://play.lebara.com/fr/en/Tamil/',
                'Connection': 'keep-alive',
            }
        data = [
                ('client_id', CLIENT_ID),
                ('client_version', CLIENT_VERSION),
                ('locale', LOCALE),
                ('timezone', TIMEZONE),
                ('os', 'nix'),
                ('os_version', '10'),
                ('type', 'desktop'),
                ('model', 'chrome'),
                ('device_id', self.device_id),
                ('name', 'nix-chrome'),
                ('access_token', self.access_token),
            ]
        print ('Registering device {}'.format(self.device_id))
        url = 'http://api.lebaraplay.com/api/v1/user/devices'
        r = requests.post(url, headers=headers, data=data)
        if r.status_code == 201:
            print ('Device succefully registered')
            self.storage_deviceinfo['registered'] = True
        else:
            print (r.json())
            if r.json()['meta']['error_type'] == 'already_linked_to_this_user':
                print ('Device aleady linked')
                self.storage_deviceinfo['registered'] = True
            else:
                print ('Erreur device registration')


    # def get_device_id(self):
    #     # Device id
    #     if self.access_token == None:
    #         print ('Error login')
    #
    #     url = 'http://api.lebaraplay.com/api/v1/user/devices'
    #
    #     params = (
    #         ('client_id', self.client_id),
    #         ('client_version', self.client_version),
    #         ('locale', self.locale),
    #         ('timezone', self.timezone),
    #         ('access_token', self.access_token),
    #     )
    #
    #     r = requests.get(url, headers=self.headers, params=params)
    #
    #     device_ids = [device['device_id'] for device in r.json()['devices'] if device['model'] in ['chrome', 'firefox']]
    #     return device_ids[0]

    def get_channels(self):

        if self.access_token == None:
            print ('Error login')

        if self.device_id == None:
            print ('Error device ID')

        chs = []
        url = 'http://play.lebara.com/fr/en/Tamil/live'
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        channels = soup.find('div', {'class': 'style-module__channels___3-Tqd'})
        for channel in channels.find_all('div', {'class': 'style-module__channel___1UCIo'}):
            name = channel.find('div', {'class': 'style-module__title___3xsjC'}).text
            channel_link = channel.find('a', {'class': 'style-module__link___2SYGt'}).get('href')
            channel_id = channel_link.split('/')[-1]
            d = {'name': name, 'url': channel_link, 'channel_id': channel_id}
            chs.append(d)

        return [channel for channel in chs if channel['name'] and channel['url'] and channel['channel_id']]

    def _get_stream_type(self, channel_id):
        # Stream TYPE

        headers = {
            'Origin': 'http://play.lebara.com',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'Referer': 'http://play.lebara.com/fr/en/Tamil/',
            'Connection': 'keep-alive',
        }

        if self.access_token == None:
            print ('Error login')

        if self.device_id == None:
            print ('Error device ID')

        url = 'http://api.lebaraplay.com/api/v1/channels/{}/stream_types'.format(channel_id)
        params = (
            ('client_id', CLIENT_ID),
            ('client_version', CLIENT_VERSION),
            ('locale', LOCALE),
            ('timezone', TIMEZONE),
            ('access_token', self.access_token),
        )

        r = requests.get(url, headers=headers, params=params)
        if r.status_code != 200:
            print ('Can not get stream type for channel {}'.format(channel_id))

        return r.json()['stream_types'][0]


    def start_heartbeat(self, hb):
        self.t = threading.Thread(target=self._heartbeat, args=(hb,))
        self.t.start()

    def _heartbeat(self, hb):
        #print ('######### in hearbeat')
        t = threading.currentThread()
        url = hb['url']
        interval = hb['interval']
        i = 0
        while (xbmc.Player().isPlayingVideo() or i < 2):
        #while (i < 1):
            #print ('##### valeur i {}'.format(i))
            print (url)
            requests.get(url)
            time.sleep(interval)
            i += 1
        print('Hearbeat stoped!!!')

    def get_stream(self, channel_id, start=None):
        # Get stream adresse
        live = False
        replay = False

        if start == None:
            live = True
        else:
            replay = True

        if not self.device_registered:
            self._register_device()

        headers = {
            'Origin': 'http://play.lebara.com',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'Referer': 'http://play.lebara.com/fr/en/Tamil/',
            'Connection': 'keep-alive',
        }

        if self.access_token == None:
            print ('Error login')

        if self.device_id == None:
            print ('Error device ID')

        stream_type = self._get_stream_type(channel_id)
        if stream_type == None:
            print ('Error get stream type')

        url = 'http://api.lebaraplay.com/api/v1/channels/{}/stream'.format(channel_id)

        params = (
            ('client_id', CLIENT_ID),
            ('client_version', CLIENT_VERSION),
            ('locale', LOCALE),
            ('timezone', TIMEZONE),
            ('screen_width', '1280'),
            ('screen_height', '720'),
            ('drm', 'clearkey'),
            ('device_id', self.device_id),
            ('id', channel_id),
            ('protocol', stream_type['protocol']),
            ('audio_codec', stream_type['audio_codec']),
            ('video_codec', stream_type['video_codec']),
            ('access_token', self.access_token),
        )

        r = requests.get(url, headers=headers, params=params)
        print (r.request)
        print (r.json())
        if r.status_code != 200:
            print ('Error requete')

        # print (r.json()['stream']['url'])
        hb = r.json()['stream']['heartbeat']


        stream_url = r.json()['stream']['url']
        if live:
            start_time = str(int(time.time()) - int(TIMEZONE) - TIMEOFFSET) + '000000'
            #print (stream_url)
            stream_url = stream_url.split('?')[0] + '?stream_req_time=' + start_time
            #print ("time.time() {}".format(time.time()))
            #print ("########## timeoffset {}".format(start_time))
            #print (stream_url)

        if replay:
            #Attention pas de decalage TIMEZONE
            start_time = str(int(start.strftime('%s')) - TIMEOFFSET) + '000000'
            stream_url = stream_url.split('?')[0] + '?stream_req_time=' + start_time

        return stream_url, hb

    def stop_stream(self):
        self.t.do_heartbeat = False
        self.t.join()

    @property
    def get_site_name(self):
        """
        set site name
        :return:
        """
        return 'lebera'

    def get_main_url(self):
        """
        site site main url
        :return:
        """
        return ''

    def get_sections(self):
        """
        get all section for tamilyogi website
        :return:
        """
        sections = [
            {
                'name': 'Live TV',
                'slug' : 'livetv'
            },
            {
                'name' : 'Replay',
                'slug' : 'replay'
            },
            {
                'name' : 'Movies',
                'slug' : 'movies'
            }]

        return [section for section in sections if section['name']]

    def get_lastweekdays(self):
        items = []
        # items.append(datetime.today().strftime('%Y-%m-%d'))
        for i in range(7):
            d = datetime.today() - timedelta(days=i)
            items.append(d.strftime('%Y-%m-%d'))

        return items

    def epg(self, channel_id, start, end):
        headers = {
            'Origin': 'http://play.lebara.com',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'Referer': 'http://play.lebara.com/fr/en/Tamil/',
            'Connection': 'keep-alive',
        }

        url = 'http://api.lebaraplay.com/api/v1/epg/events?client_id=spbtv-web&client_version=0.1.0&locale=en_GB&timezone=7' \
              '200&limit=100&channels[]={}&from_date={}&to_date={}'.format(
            channel_id, start, end
        )

        print ('selected date {}'.format(url))
        r = requests.get(url, headers=headers)

        return r.json()['events']