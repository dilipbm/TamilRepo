import requests

class Omdb(object):
    api_key = None

    def __init__(self, api_key):
        self.api_key = api_key


    def get_movie_info(self, title=None, year=None):
        params = (
            ('t', title),
            ('y', year),
            ('apikey', self.api_key)
        )
        url = 'http://www.omdbapi.com/'
        r = requests.get(url, params=params)
        if r.status_code == 200:
            return r.json()
        else:
            return None

if __name__ == '__main__':
    api_key = 'eaf23cbd'
    mu = Omdb(api_key)
    r = mu.get_movie_info(title='Mersal', year='2017')
