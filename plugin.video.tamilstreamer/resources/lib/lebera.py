import helper
import urllib2
import stream_resolver
from xbmcswift2 import xbmc
from datetime import datetime, timedelta

'''
    Main API for lebera site
'''

addon_id = 'plugin.video.tamilstreamer'
icon_next = xbmc.translatePath('special://home/addons/{0}/resources/images/next.png'.format(addon_id))


class Lebera(object):
    def __init__(self, plugin):
        self.plugin = plugin

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
                        'url': ''
                    },
                    {
                        'name': 'Movies',
                        'url': ''
                    }]

        return [section for section in sections if section['name']]

    def get_channels(self):
        items = [
            {'name' : 'Vilay TV',
             'id' : 'idvijay'}
        ]

        return items


    def get_lastweekdays(self):
        items = []
        #items.append(datetime.today().strftime('%Y-%m-%d'))
        for i in range(7):
            d = datetime.today() - timedelta(days=i)
            items.append(d.strftime('%Y-%m-%d'))

        return items
