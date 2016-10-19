from xbmcswift2 import Plugin
from resources.lib import api_tamilyogi as api_tamilyogi

plugin = Plugin()


# SITE VIEW
@plugin.route('/')
def index():
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
    if site_name == 'tamilyogi':
        api = api_tamilyogi.TamilYogi()
        sections = api.get_sections()

    items = [{
                 'label': section['name'],
                 'path': plugin.url_for('movies_view', site_name=site_name, section_url=section['url']),
             } for section in sections]

    return items


# MOVIES VIEW
@plugin.route('/movies/<site_name>/<section_url>')
def movies_view(site_name, section_url):
    if site_name == 'tamilyogi':
        api = api_tamilyogi.TamilYogi()
        movies = api.get_movies(section_url)

    items = [{
                 'label': movie['name'],
                 'path': plugin.url_for('stream_list_view', movie_name=movie['name'], movie_url=movie['url'])
             } for movie in movies]

    return items


# STREAM LIST VIEW
@plugin.route('/stream_list/<movie_name>/<movie_url>')
def stream_list_view(movie_name, movie_url):
    api = api_tamilyogi.TamilYogi()
    stream_urls = api.get_stream_urls(movie_name, movie_url)

    items = [{'label': 'Play - ' + stream_url['name'] + ' - ' + stream_url['quality'],
              'path': plugin.url_for('play_lecture', movie_name=stream_url['name'], stream_url=stream_url['url']),
              'is_playable': True} for stream_url in stream_urls]

    return items


#   if len(stream_urls) > 1:
#       items = [{'label': 'Play - ' + stream_url['name'] + ' - ' + stream_url['quality'],
#               'path': plugin.url_for('play_lecture', movie_name=stream_url['name'], stream_url=stream_url['url']),
#               'is_playable': True} for stream_url in stream_urls]
#
#        return items
#
#    else :
#        plugin.log.info('Playing url: %s' % stream_urls[0]['url'])
#        plugin.set_resolved_url(stream_urls[0]['url'])


@plugin.route('/lectures/<stream_url>/')
def play_lecture(stream_url):
    plugin.log.info('Playing url: %s' % stream_url)
    plugin.set_resolved_url(stream_url)


if __name__ == '__main__':
    plugin.run()
