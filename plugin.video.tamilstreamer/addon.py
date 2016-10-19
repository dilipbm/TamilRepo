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
                 'path': plugin.url_for('movies_view', site_name=site_name, url=section['url']),
             } for section in sections]

    return items


# MOVIES VIEW
@plugin.route('/movies/<site_name>/<url>')
def movies_view(site_name, url):
    if site_name == 'tamilyogi':
        api = api_tamilyogi.TamilYogi()
        print url
        movies = api.get_movies(url)

    items = [{
                 'label': movie['name'],
                 'path': movie['url'],
                'is_playable': True
             } for movie in movies]

    return items

# Lecture
#@plugin.route('/lectures/<url>/')
#def play_lecture(url):
#    item = {'label': 'Movie',
#            'path': url,
#            'is_playable': True
#            }

#   return [item]


if __name__ == '__main__':
    plugin.run()
