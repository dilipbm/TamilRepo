from xbmcswift2 import Plugin, ListItem, xbmc, xbmcgui
from resources.lib import tamilyogi, tamilrasigan, lebera, tamilgun, thiraimix
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

        {
            'label': 'Tamilgun',
            'path': plugin.url_for('section_view', site_name='tamilgun')
        },

        {
            'label': 'ThiraiMix',
            'path': plugin.url_for('section_view', site_name='thiraimix')
        }

        #{'label' : 'Lebera',
        # 'path' : plugin.url_for('section_view', site_name='lebera'),
        #},

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
        site_api.manage_connexion()
        items = []
        sections = site_api.get_sections()

        for section in sections:
            print (section)
            if section['slug'] == 'livetv':
                d = {'label': section['name'], 'path': plugin.url_for('channels_view', refer=section['slug'])}
                items.append(d)
            elif section['slug'] == 'replay':
                d = {'label': section['name'], 'path': plugin.url_for('channels_view', refer=section['slug'])}
                items.append(d)
    
    if site_name == 'tamilgun':
        site_api = tamilgun.Tamilgun(plugin)
        items = [{
                     'label': section['name'],
                     'path': plugin.url_for('movies_view', site_name=site_name, section_url=section['url']),
                 } for section in site_api.get_sections()]

    if site_name == 'thiraimix':
        site_api = thiraimix.Thiraimix(plugin)
        items = [{
                     'label': section['name'],
                     'path': plugin.url_for('programmes_view', site_name=site_name, url=section['url']),
                 } for section in site_api.get_sections()]

    return items


@plugin.route('/programmes/<site_name>/<url>')
def programmes_view(site_name, url):
    plugin.set_content('tvshows')

    if site_name == 'thiraimix':
        site_api = thiraimix.Thiraimix(plugin)
        programmes = site_api.get_programmes(url)

    items = [{
                 'label': programme['name'],
                 'thumbnail': programme['image'],
                 'path': plugin.url_for('episode_view', site_name=site_name, url=programme['url'])
             } for programme in programmes]

    return items



@plugin.route('/episodes/<site_name>/<url>')
def episode_view(site_name, url):
    plugin.set_content('files')

    if site_name == 'thiraimix':
        site_api = thiraimix.Thiraimix(plugin)
        episodes = site_api.get_episodes(url)

    items = [{
                 'label': episode['name'],
                 'path': plugin.url_for('stream_list_view', site_name=site_name, movie_name=episode['prog_name'], movie_url=episode['url'])
             } for episode in episodes]

    return items


@plugin.route('/epg/<date>/<channel_id>')
def epg_view(date, channel_id):
    start = str(date) + 'T00:00:00.000Z'
    end = str(date) + 'T23:30:00.000Z'
    site_api = lebera.Lebera(plugin)
    events = site_api.epg(channel_id, start, end)

    plugin.set_content('tvshows')

    items = [{
                 'label': event['label'],
                 'icon': event['image_url'],
                 'path': plugin.url_for('lebera_play', channel_name='chname', channel_id=event['channel_id'],
                                   start=event['start_date']),
             } for event in events]

    return items


@plugin.route('/week/<channel_id>/<channel_name>')
def week_view(channel_id, channel_name):
    site_api = lebera.Lebera(plugin)
    print (site_api.get_lastweekdays())
    print (type(site_api.get_lastweekdays()[0]))
    items = [{
                 'label': day,
                 'path': plugin.url_for('epg_view', date=day, channel_id=channel_id),
             } for day in site_api.get_lastweekdays()]

    return items

@plugin.route('/channels/<refer>')
def channels_view(refer):
    site_api = lebera.Lebera(plugin)
    #stime = site_api.live_startime()

    #print ('Starttime {0}'.format(stime))

    if refer == 'livetv':
        items = [{
                 'label': channel['name'],
                 'path': plugin.url_for('lebera_play', channel_name=channel['name'], channel_id=channel['channel_id'], start='live'),
             } for channel in site_api.get_channels()]

    elif refer == 'replay':
        items = [{
                     'label': channel['name'],
                     'path': plugin.url_for('week_view', channel_name=channel['name'],
                                            channel_id=channel['channel_id']),
                 } for channel in site_api.get_channels()]


    return items

@plugin.route('/lebera_play/<channel_name>/<channel_id>/<start>')
def lebera_play(channel_name, channel_id, start):
    site_api = lebera.Lebera(plugin)
    stime = None

    print ("############# replay start {0}".format(start))

    if start != 'None':

        if start == 'live':
            stream_url, heartbeat = site_api.get_stream(channel_id, stime)

        else:

            try:
                stime = datetime.strptime(start, '%Y-%m-%dT%H:%M:%SZ')
            except TypeError:
                stime = datetime(*(timee.strptime(start, '%Y-%m-%dT%H:%M:%SZ')[0:6]))

            stream_url, heartbeat = site_api.get_stream(channel_id, stime)

        item = {
            'label': channel_name,
            'path': stream_url,
        }

        plugin.play_video(item)
        site_api.start_heartbeat(heartbeat)

    else:
        plugin.notify(msg='You cannot play this video', title='Error replay')


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

    if site_name == 'tamilgun':
        site_api = tamilgun.Tamilgun(plugin)

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

        if site_name == 'tamilrasigan':
            site_api = tamilrasigan.TamilRasigan(plugin)

        if site_name == 'tamilgun':
            site_api = tamilgun.Tamilgun(plugin)

        if site_name == 'thiraimix':
            site_api = thiraimix.Thiraimix(plugin)

        stream_urls = site_api.get_stream_urls(movie_name, movie_url)

        if len(stream_urls) == 0:
            plugin.notify(msg=movie_name, title='Video is no longer available')

        #elif len(stream_urls) == 1:
        #    print ('One stream urls %s' %stream_urls[0]['url'])
        #    plugin.set_resolved_url(stream_urls[0]['url'])

        else:
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
    plugin.log.info('####### Playing url: %s' % stream_url)
    plugin.set_resolved_url(stream_url)
    #plugin.notify(msg=movie_name, title='Now Playing')




if __name__ == '__main__':
    plugin.run()


