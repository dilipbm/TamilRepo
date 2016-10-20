from xbmcswift2 import Plugin
from resources.lib import api_tamilyogi

plugin = Plugin()
api = api_tamilyogi.TamilYogi()


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
        sections = api.get_sections()

    items = [{
                 'label': section['name'],
                 'path': plugin.url_for('movies_view', section_url=section['url']),
             } for section in sections]

    return items


# MOVIES VIEW
@plugin.route('/movies/<section_url>')
def movies_view(section_url):
    movies = api.get_movies(section_url)
    plugin.set_view_mode(500)

    items = [{
                 'label': movie['name'],
                 'thumbnail': movie['image'],
                 'path': plugin.url_for('stream_list_view', movie_name=movie['name'], movie_url=movie['url'])
             } for movie in movies]

    return items


# STREAM LIST VIEW
@plugin.route('/stream_list/<movie_name>/<movie_url>')
def stream_list_view(movie_name, movie_url):
    # If Next Page
    if movie_name == 'Next Page':
        plugin.redirect(plugin.url_for('movies_view', section_url=movie_url))

    else:
        stream_urls = api.get_stream_urls(movie_name, movie_url)

        items = [{'label': 'Play - ' + stream_url['name'] + ' - ' + stream_url['quality'],
                  'path': plugin.url_for('play_lecture', movie_name=stream_url['name'], stream_url=stream_url['url']),
                  'is_playable': True} for stream_url in stream_urls]
        return items

#        if len(stream_urls) == 1:
#            stream_url = stream_urls[0]['url']
#            plugin.set_resolved_url(stream_url)
            #plugin.redirect(plugin.url_for('play_lecture', stream_url=stream_urls[0]['url']))


#        elif len(stream_urls) > 1:
#            items = [{'label': 'Play - ' + stream_url['name'] + ' - ' + stream_url['quality'],
#                      'path': plugin.url_for('play_lecture', movie_name=stream_url['name'], stream_url=stream_url['url']),
#                      'is_playable': True} for stream_url in stream_urls]
#            return items


@plugin.route('/lectures/<movie_name>/<stream_url>/')
def play_lecture(movie_name, stream_url):
    plugin.log.info('Playing url: %s' % stream_url)
    plugin.set_resolved_url(stream_url)
    plugin.notify(msg=movie_name, title='Now Playing')


if __name__ == '__main__':
    plugin.run()
