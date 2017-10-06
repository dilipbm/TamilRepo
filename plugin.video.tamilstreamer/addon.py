from xbmcswift2 import Plugin, ListItem, xbmc, xbmcgui
from resources.lib import tamilyogi, tamilrasigan, lebera
import pprint
from datetime import datetime, timedelta
import ast
import time as timee
plugin = Plugin()


# SITE VIEW - MAIN VIEW
@plugin.route('/')
def index():
    """
    All site here
    :return:
    """

    plugin.set_content('files')

    items = [
        {'label': 'Tamil Yogi',
         'path': plugin.url_for('section_view', site_name='tamilyogi')},

        {'label': 'Tamil Rasigan',
         'path': plugin.url_for('section_view', site_name='tamilrasigan')},

        {'label' : 'Lebera',
         'path' : plugin.url_for('section_view', site_name='lebera'),
        }
    ]
    return items


# SECTION VIEW
@plugin.route('/sections/<site_name>')
def section_view(site_name):
    """
    all sections by sites. sections are getted from site api
    :param site_name:
    :return:
    """

    plugin.set_content('files')

    if site_name == 'tamilyogi':
        site_api = tamilyogi.TamilYogi(plugin)
        items = [{
                     'label': section['name'],
                     'path': plugin.url_for('movies_view', site_name=site_name, section_url=section['url']),
                 } for section in site_api.get_sections()]

    if site_name == 'tamilrasigan':
        site_api = tamilrasigan.TamilRasigan(plugin)
        items = [{
                     'label': section['name'],
                     'path': plugin.url_for('movies_view', site_name=site_name, section_url=section['url']),
                 } for section in site_api.get_sections()]

    if site_name == 'lebera':
        site_api = lebera.Lebera(plugin)
        site_api._login()
        items = []
        sections = site_api.get_sections()

        for section in sections:
             print (section)
             if section['slug'] == 'livetv':
                 d = {'label': section['name'], 'path': plugin.url_for('channels_view', refer=section['slug'])}
                 items.append(d)

        #if section['name'] == 'Movies':
        #    d = {'label': section['name'], 'path': plugin.url_for('movies_view', site_name=site_name)}
        #    items.append(d)

    return items


@plugin.route('/epg/<date>')
def epg_view(date):
    start = datetime.strptime(date, '%Y-%m-%dT00:00:00.000Z')
    end = datetime.strptime(date, '%Y-%m-%dT23:30:00.000Z')
    url = 'http://api.lebaraplay.com/api/v1/epg/events?client_id=spbtv-web&client_version=0.1.0&locale=en_GB&timezone=7200&channels[]=maa-channel-2-43707b&from_date={}&to_date={}'.format(
        start, end
    )

    print ('selected date {}'.format(url))


@plugin.route('/week/')
def week_view():
    site_api = lebera.Lebera(plugin)
    print (site_api.get_lastweekdays())
    items = [{
                 'label': day,
                 'path': plugin.url_for('epg_view', date=day),
             } for day in site_api.get_lastweekdays()]

    return items

@plugin.route('/channels/<refer>')
def channels_view(refer):
    site_api = lebera.Lebera(plugin)

    if refer == 'livetv':
        items = [{
                 'label': channel['name'],
                 'path': plugin.url_for('lebera_play', channel_name=channel['name'], channel_id=channel['channel_id']),
             } for channel in site_api.get_channels()]

    return items

@plugin.route('/lebera_play/<channel_name>/<channel_id>')
def lebera_play(channel_name, channel_id):
    site_api = lebera.Lebera(plugin)
    stream_url, heartbeat = site_api.get_stream(channel_id, live=True)

    print ('OK stream url got : {}'.format(stream_url))

    item = {
        'label': channel_name,
        'path': stream_url,
    }

    print ('######## Start to play')
    plugin.play_video(item)
    print ('######## OK to player start heartbeat')
    site_api.heartbeat(heartbeat)


    #return [{
    #    'label' : 'Play',
    #    'path': plugin.url_for('lebera_lecture', stream_url=stream_url, heartbeat=str(heartbeat)),
    #    'is_playable': True
    #}]
    #plugin.redirect(plugin.url_for('play_lecture', movie_name=channel_name, stream_url=stream_url))


# MOVIES VIEW
@plugin.route('/movies/<site_name>/<section_url>')
def movies_view(site_name, section_url):
    """
    show all movies from url (section_url).
    :param site_name:
    :param section_url:
    :return:
    """
    if site_name == 'tamilyogi':
        site_api = tamilyogi.TamilYogi(plugin)

    if site_name == 'tamilrasigan':
        site_api = tamilrasigan.TamilRasigan(plugin)

    movies = site_api.get_movies(section_url)
    # plugin.set_view_mode(500)
    plugin.set_content('musicvideos')
    #   for movie in movies:
    #       print movie['image']

    #plugin.get_view_mode_id('wall')

    items = [{
                 'label': movie['name'],
                 'thumbnail': movie['image'],
                 'info': movie['infos'],
                 'path': plugin.url_for('stream_list_view', site_name=site_name, movie_name=movie['name'],
                                        movie_url=movie['url'])
             } for movie in movies]

    return items


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

    plugin.set_content('files')

    # If hit Next page
    if movie_name == 'Next Page':
        plugin.redirect(plugin.url_for('movies_view', site_name=site_name, section_url=movie_url))

    else:
        if site_name == 'tamilyogi':
            site_api = tamilyogi.TamilYogi(plugin)
        stream_urls = site_api.get_stream_urls(movie_name, movie_url)
        items = [{'label': stream_url['name'] + ' | ' + stream_url['quality'],
                  'label2': stream_url['quality'],
                  'icon': stream_url['quality_icon'],
                  'path': plugin.url_for('play_lecture', movie_name=stream_url['name'], stream_url=stream_url['url']),
                  'is_playable': True} for stream_url in stream_urls]
        return items


# @plugin.route('/lebera_lecture/<stream_url>/<heartbeat>/')
# def lebera_lecture(stream_url, heartbeat):
#     print ('####### in lecture')
#     print (type(heartbeat))
#     print (stream_url)
#     print (heartbeat)
#
#     plugin.set_resolved_url(stream_url)
#     site_api = lebera.Lebera(plugin)
#     site_api.heartbeat(ast.literal_eval(heartbeat))


@plugin.route('/lectures/<movie_name>/<stream_url>/')
def play_lecture(movie_name, stream_url):
    """
    Stream movie
    :param movie_name:
    :param stream_url:
    :return:
    """

    plugin.log.info('Playing url: %s' % stream_url)
    plugin.set_resolved_url(stream_url)
    #plugin.notify(msg=movie_name, title='Now Playing')




if __name__ == '__main__':
    plugin.run()


