import pprint
from datetime import datetime, timedelta
import ast
import time as timee

import routing
import xbmcgui
from xbmcgui import ListItem
from xbmcplugin import addDirectoryItem, endOfDirectory, setResolvedUrl, setContent

from resources.lib import tamilyogi
from resources.lib import tamilrasigan
from resources.lib import tamilgun
from resources.lib import thiraimix
from resources.lib import helper as hp

plugin = routing.Plugin()


# SITE VIEW - MAIN VIEW
@plugin.route('/')
def index():
    """
    All site here
    :return:
    """

    addDirectoryItem(plugin.handle, plugin.url_for(section_view, site_name="tamilyogi"), ListItem("Tamil Yogi"), True)
    addDirectoryItem(plugin.handle, plugin.url_for(section_view, site_name="tamilgun"), ListItem("Tamilgun"), True)
    #addDirectoryItem(plugin.handle, plugin.url_for(section_view, site_name="thiraimix"), ListItem("ThiraiMix"), True)

    endOfDirectory(plugin.handle)


# SECTION VIEW
@plugin.route('/sections/<site_name>')
def section_view(site_name):
    """
    all sections by sites. sections are getted from site api
    :param site_name:
    :return:
    """


    if site_name == 'tamilyogi':
        site_api = tamilyogi.TamilYogi(plugin)

        
        for section in site_api.get_sections():
        
            addDirectoryItem(
                plugin.handle,
                plugin.url_for(movies_view, site_name=site_name, section_url=hp.encode_url(section['url'])),
                ListItem(section['name']), 
                True)

        endOfDirectory(plugin.handle) 

    elif site_name == 'tamilrasigan':
        site_api = tamilrasigan.TamilRasigan(plugin)

        for section in site_api.get_sections():
            addDirectoryItem(
                plugin.handle,
                plugin.url_for(movies_view, site_name=site_name, section_url=hp.encode_url(section['url'])),
                ListItem(section['name']), 
                True)

        endOfDirectory(plugin.handle) 


    elif site_name == 'thiraimix':
        site_api = thiraimix.Thiraimix(plugin)
        for section in site_api.get_sections():
            addDirectoryItem(plugin.handle,
            plugin.url_for(movies_view, site_name=site_name, section_url=hp.encode_url(section['url'])),
            ListItem(section['name']),
            True)

        endOfDirectory(plugin.handle) 
    
    elif site_name == 'tamilgun':
        site_api = tamilgun.Tamilgun(plugin)
        for section in site_api.get_sections():
            addDirectoryItem(plugin.handle,
            plugin.url_for(movies_view, site_name=site_name, section_url=hp.encode_url(section['url'])),
            ListItem(section['name']),
            True)

        endOfDirectory(plugin.handle) 

    else:
        endOfDirectory(plugin.handle) 



@plugin.route('/programmes/<site_name>/<url>')
def programmes_view(site_name, url):

    if site_name == 'thiraimix':
        site_api = thiraimix.Thiraimix(plugin)
        programmes = site_api.get_programmes(url)


    for programme in programmes:
        listitem = ListItem(programme['name'])
        listitem.setThumbnailImage(programme['image'])
        addDirectoryItem (
            plugin.handle, 
            plugin.url_for(episode_view, site_name=site_name, url=hp.encode_url(programme['url'])), 
            listitem,
            True
        )

    endOfDirectory(plugin.handle) 



@plugin.route('/episodes/<site_name>/<url>')
def episode_view(site_name, url):

    if site_name == 'thiraimix':
        site_api = thiraimix.Thiraimix(plugin)
        episodes = site_api.get_episodes(url)


    for episode in episodes:
        addDirectoryItem (
            plugin.handle, 
            plugin.url_for(stream_list_view, site_name=site_name, movie_name=episode['prog_name'], movie_url=hp.encode_url(episode['url'])), 
            ListItem(episode['name']),
            True
        )

    endOfDirectory(plugin.handle)


# MOVIES VIEW
@plugin.route('/movies/<site_name>/<section_url>')
def movies_view(site_name, section_url):
    """
    show all movies from url (section_url).
    :param site_name:
    :param section_url:
    :return:
    """

    section_url = hp.decode_url(section_url)

    if site_name == 'tamilyogi':
        site_api = tamilyogi.TamilYogi(plugin)

    if site_name == 'tamilrasigan':
        site_api = tamilrasigan.TamilRasigan(plugin)

    if site_name == 'tamilgun':
        site_api = tamilgun.Tamilgun(plugin)

    movies = site_api.get_movies(section_url)


    for movie in movies:
        listitem = ListItem(movie['name'])
        listitem.setThumbnailImage(movie['image'])
        listitem.setArt({
            'thumb': movie['image'],
            'poster': movie['image']
        })
        listitem.setInfo('video', movie['infos'])
        addDirectoryItem (
            plugin.handle, 
            plugin.url_for(stream_list_view, site_name=site_name, movie_name=movie['name'], movie_url=hp.encode_url(movie['url'])), 
            listitem,
            True
        )

    setContent(plugin.handle, 'movies')
    endOfDirectory(plugin.handle)


# STREAM LIST VIEW
@plugin.route('/stream_list/<site_name>/<movie_name>/<movie_url>')
def stream_list_view(site_name, movie_name, movie_url):
    """
    show all stream for the movie with quality
    :param site_name:
    :param movie_name:
    :param movie_url:
    :return:
    """

    movie_url = hp.decode_url(movie_url)

    # If hit Next page
    if movie_name == 'Next Page':
        plugin.redirect('/movies/{}/{}'.format(site_name,hp.encode_url(movie_url)))

    else:
        if site_name == 'tamilyogi':
            site_api = tamilyogi.TamilYogi(plugin)

        if site_name == 'tamilrasigan':
            site_api = tamilrasigan.TamilRasigan(plugin)

        if site_name == 'tamilgun':
            site_api = tamilgun.Tamilgun(plugin)

        if site_name == 'thiraimix':
            site_api = thiraimix.Thiraimix(plugin)

        stream_urls = site_api.get_stream_urls(movie_name, movie_url)

        if len(stream_urls) == 0:
            xbmcgui.Dialog().notification(heading='Error 404', message='Video is no longer available')

        else:
            for stream_url in stream_urls:
                print('>>>>>>>>>>>>>>>> {}'.format(stream_url['url']))
                listitem = ListItem(stream_url['name'] + ' | ' + stream_url['quality'])
                listitem.setInfo(type='video', infoLabels={'Title': stream_url['name'] })
                listitem.setIconImage(stream_url['quality_icon'])
                listitem.setProperty('IsPlayable', 'true')
                addDirectoryItem (
                    plugin.handle, 
                    stream_url['url'],
                    listitem,
                    False
                )

            endOfDirectory(plugin.handle) 



if __name__ == '__main__':
    plugin.run()


