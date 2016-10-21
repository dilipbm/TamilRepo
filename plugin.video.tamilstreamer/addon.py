from xbmcswift2 import Plugin
from resources.lib import tamilyogi
import pprint

plugin = Plugin()

icon_720 = 'https://raw.githubusercontent.com/dilipbm/TamilRepo/master/plugin.video.tamilstreamer/resources/images/icon_720.png'
icon_360 = 'https://raw.githubusercontent.com/dilipbm/TamilRepo/master/plugin.video.tamilstreamer/resources/images/icon_360.png'
icon_240 = 'https://raw.githubusercontent.com/dilipbm/TamilRepo/master/plugin.video.tamilstreamer/resources/images/icon_240.png'

# SITE VIEW - MAIN VIEW
@plugin.route('/')
def index():
    """
    All site here
    :return:
    """
    items = [
        {'label': 'Tamil Yogi',
         'path': plugin.url_for('section_view', site_name='tamilyogi')},

        {'label': 'Tamil Gun',
         'path': plugin.url_for('section_view', site_name='tamilgun')},
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

    if site_name == 'tamilyogi':
        site_api = tamilyogi.TamilYogi()

    sections = site_api.get_sections()

    items = [{
                 'label': section['name'],
                 'path': plugin.url_for('movies_view', site_name=site_name, section_url=section['url']),
             } for section in sections]

    return items


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
        site_api = tamilyogi.TamilYogi()

    movies = site_api.get_movies(section_url)
    plugin.set_view_mode(500)
    for movie in movies:
        print movie['image']

    items = [{
                 'label': movie['name'],
                 'thumbnail': movie['image'],
                 'path': plugin.url_for('stream_list_view', site_name=site_name, movie_name=movie['name'], movie_url=movie['url'])
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

    plugin.set_view_mode(512)

    # If hit Next page
    if movie_name == 'Next Page':
        plugin.redirect(plugin.url_for('movies_view', site_name=site_name, section_url=movie_url))

    else:
        if site_name == 'tamilyogi':
            site_api = tamilyogi.TamilYogi()
        stream_urls = site_api.get_stream_urls(movie_name, movie_url)
        items = [{'label': 'Play - ' + stream_url['name'] + '    ' + stream_url['quality'],
                  'label2': stream_url['quality'],
                  #'icon':'icon_'+stream_url['quality'].replace('p',''),
                  'path': plugin.url_for('play_lecture', movie_name=stream_url['name'], stream_url=stream_url['url']),
                  'is_playable': True} for stream_url in stream_urls]
        return items


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
    plugin.notify(msg=movie_name, title='Now Playing')


if __name__ == '__main__':
    plugin.run()
