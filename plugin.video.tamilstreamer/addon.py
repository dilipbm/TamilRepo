import pprint
from datetime import datetime, timedelta
import ast
import time as timee
import re

import routing
import xbmcgui
from xbmcgui import ListItem
from xbmcplugin import addDirectoryItem, endOfDirectory, setResolvedUrl, setContent

from resources.lib import tamilyogi
from resources.lib import tamilrasigan
from resources.lib import tamilgun
from resources.lib import tamildbox
from resources.lib import thiraimix
from resources.lib import tamilarasan
from resources.lib import tamildhool
from resources.lib import utils

plugin = routing.Plugin()


# SITE VIEW - MAIN VIEW
@plugin.route('/')
def index():
    """
    All site here
    :return:
    """

    addDirectoryItem(plugin.handle, plugin.url_for(
        section_view, site_name="tamilyogi"), ListItem("Tamil Yogi"), True)
    addDirectoryItem(plugin.handle, plugin.url_for(
        section_view, site_name="tamilgun"), ListItem("Tamilgun"), True)
    addDirectoryItem(plugin.handle, plugin.url_for(
        section_view, site_name="tamildbox"), ListItem("Tamildbox"), True)
    #addDirectoryItem(plugin.handle, plugin.url_for(section_view, site_name="thiraimix"), ListItem("ThiraiMix"), True)
    addDirectoryItem(plugin.handle, plugin.url_for(
        section_view, site_name="tamilarasan"), ListItem("Tamilarasan"), True)
    addDirectoryItem(plugin.handle, plugin.url_for(
        section_view, site_name="tamildhool"), ListItem("TamilDhool"), True)

    # addDirectoryItem(plugin.handle, plugin.url_for(
    #    directplay), ListItem("Test"), True)

    endOfDirectory(plugin.handle)


# SECTION VIEW
@plugin.route('/sections/<site_name>')
def section_view(site_name):
    """
    all sections by sites. sections are getted from site api
    :param site_name:
    :return:
    """

    setContent(plugin.handle, 'files')

    if site_name == 'tamilyogi':
        site_api = tamilyogi.TamilYogi(plugin)

        for section in site_api.get_sections():
            addDirectoryItem(
                plugin.handle,
                plugin.url_for(movies_view, site_name=site_name,
                               section_url=utils.encode_url(section['url'])),
                ListItem(section['name']),
                True)

    elif site_name == 'tamilrasigan':
        site_api = tamilrasigan.TamilRasigan(plugin)

        for section in site_api.get_sections():
            addDirectoryItem(
                plugin.handle,
                plugin.url_for(movies_view, site_name=site_name,
                               section_url=utils.encode_url(section['url'])),
                ListItem(section['name']),
                True)

    elif site_name == 'thiraimix':
        site_api = thiraimix.Thiraimix(plugin)
        for section in site_api.get_sections():
            addDirectoryItem(plugin.handle,
                             plugin.url_for(
                                 movies_view, site_name=site_name, section_url=utils.encode_url(section['url'])),
                             ListItem(section['name']),
                             True)

    elif site_name == 'tamilgun':
        site_api = tamilgun.Tamilgun(plugin)
        for section in site_api.get_sections():
            addDirectoryItem(plugin.handle,
                             plugin.url_for(
                                 movies_view, site_name=site_name, section_url=utils.encode_url(section['url'])),
                             ListItem(section['name']),
                             True)

    elif site_name == 'tamildbox':
        site_api = tamildbox.Tamildbox(plugin)
        for section in site_api.get_sections():
            addDirectoryItem(plugin.handle,
                             plugin.url_for(
                                 movies_view, site_name=site_name, section_url=utils.encode_url(section['url'])),
                             ListItem(section['name']),
                             True)

    elif site_name == 'tamilarasan':
        site_api = tamilarasan.Tamilarasan(plugin)
        for section in site_api.get_sections():
            addDirectoryItem(plugin.handle,
                             plugin.url_for(
                                 movies_view, site_name=site_name, section_url=utils.encode_url(section['url'])),
                             ListItem(section['name']),
                             True)

    elif site_name == 'tamildhool':
        site_api = tamildhool.TamilDhool(plugin)
        for section in site_api.get_sections():
            addDirectoryItem(plugin.handle,
                             plugin.url_for(
                                 programmes_view, site_name=site_name, url=utils.encode_url(section['url'])),
                             ListItem(section['name']),
                             True)

    endOfDirectory(plugin.handle)


@plugin.route('/programmes/<site_name>/<url>')
def programmes_view(site_name, url):

    url = utils.decode_url(url)

    if site_name == 'thiraimix':
        site_api = thiraimix.Thiraimix(plugin)
        programmes = site_api.get_programmes(url)

    elif site_name == 'tamildhool':
        site_api = tamildhool.TamilDhool(plugin)
        programmes = site_api.get_programmes(url)

    for programme in programmes:
        listitem = ListItem(programme['name'])
        listitem.setThumbnailImage(programme['image'])
        addDirectoryItem(
            plugin.handle,
            plugin.url_for(episode_view, site_name=site_name,
                           url=utils.encode_url(programme['url'])),
            listitem,
            True
        )

    endOfDirectory(plugin.handle)


@plugin.route('/episodes/<site_name>/<url>')
def episode_view(site_name, url):

    url = utils.decode_url(url)

    if site_name == 'thiraimix':
        site_api = thiraimix.Thiraimix(plugin)
        episodes = site_api.get_episodes(url)

    elif site_name == 'tamildhool':
        site_api = tamildhool.TamilDhool(plugin)
        episodes = site_api.get_episodes(url)

    for episode in episodes:
        addDirectoryItem(
            plugin.handle,
            plugin.url_for(stream_list_view, site_name=site_name,
                           movie_name=episode['prog_name'], movie_url=utils.encode_url(episode['url'])),
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

    setContent(plugin.handle, 'movies')

    section_url = utils.decode_url(section_url)

    if site_name == 'tamilyogi':
        site_api = tamilyogi.TamilYogi(plugin)

    elif site_name == 'tamilrasigan':
        site_api = tamilrasigan.TamilRasigan(plugin)

    elif site_name == 'tamilgun':
        site_api = tamilgun.Tamilgun(plugin)

    elif site_name == 'tamildbox':
        site_api = tamildbox.Tamildbox(plugin)

    elif site_name == 'tamilarasan':
        site_api = tamilarasan.Tamilarasan(plugin)

    elif site_name == 'tamildhool':
        site_api = tamildhool.TamilDhool(plugin)

    movies = site_api.get_movies(section_url)

    if len(movies) == 0:
        xbmcgui.Dialog().notification("Error 404", "No movies found")
        setContent(plugin.handle, 'files')
        plugin.redirect('/sections/{}'.format(site_name))

    for movie in movies:
        listitem = ListItem(utils.color_movie_name(movie['name']))
        listitem.setThumbnailImage(movie['image'])
        listitem.setArt({
            'thumb': movie['image'],
            'poster': movie['image']
        })
        listitem.setInfo('video', movie['infos'])
        addDirectoryItem(
            plugin.handle,
            plugin.url_for(stream_list_view, site_name=site_name,
                           movie_name=movie['name'], movie_url=utils.encode_url(movie['url'])),
            listitem,
            True
        )

    endOfDirectory(plugin.handle)


@plugin.route('/directplay')
def directplay():
    listitem = ListItem('test')
    listitem.setProperty('IsPlayable', 'true')
    # addDirectoryItem(
    #    plugin.handle,
    #    'https://www1411.hlsmp4.com/token=RYov85oqYWpHg890KDQYiQ/1559514826/0.0.0.0/47/6/bb/cb0147d55dfd8f9e3b9b793083480bb6-720p.mp4',
    #    listitem,
    #    False
    # )

    addDirectoryItem(
        plugin.handle,
        'https://www.malarmoon.com/v/AlnkhFF.m3u8',
        listitem,
        False
    )

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

    movie_url = utils.decode_url(movie_url)

    # If hit Next page
    if movie_name == 'Next Page':
        plugin.redirect('/movies/{}/{}'.format(site_name,
                                               utils.encode_url(movie_url)))

    else:
        if site_name == 'tamilyogi':
            site_api = tamilyogi.TamilYogi(plugin)

        elif site_name == 'tamilrasigan':
            site_api = tamilrasigan.TamilRasigan(plugin)

        elif site_name == 'tamilgun':
            site_api = tamilgun.Tamilgun(plugin)

        elif site_name == 'thiraimix':
            site_api = thiraimix.Thiraimix(plugin)

        elif site_name == 'tamildbox':
            site_api = tamildbox.Tamildbox(plugin)

        elif site_name == 'tamilarasan':
            site_api = tamilarasan.Tamilarasan(plugin)

        elif site_name == 'tamildhool':
            site_api = tamildhool.TamilDhool(plugin)

        stream_urls = site_api.get_stream_urls(movie_name, movie_url)

        if len(stream_urls) == 0:
            xbmcgui.Dialog().notification(heading='Error 404',
                                          message='Video is no longer available')

        else:
            for stream_url in stream_urls:
                listitem = ListItem(
                    stream_url['name'] + ' | ' + stream_url['quality'])
                listitem.setInfo(type='video', infoLabels={
                                 'Title': stream_url['name']})
                listitem.setIconImage(stream_url['quality_icon'])
                listitem.setProperty('IsPlayable', 'true')
                addDirectoryItem(
                    plugin.handle,
                    stream_url['url'],
                    listitem,
                    False
                )

            endOfDirectory(plugin.handle)


if __name__ == '__main__':
    plugin.run()
