import re
import helper as helper
import pprint
import json


# To load Vidmad Video stream url
def load_vidmad_video(url):
    soup = helper.get_soup_from_url(url)
    script = soup.find_all('script', type="text/javascript")
    # regex = re.compile('file:"(.*?),')
    # regex = re.compile('sources:(.*?)image')
    regex = re.compile('file:(.*?)}')
    videofiles = re.findall(regex, str(script))
    items = []
    for video in videofiles:
        url = None
        quality = 'default'

        try:
            url = video.split('"')[1]
            quality = video.split('"')[3]
        except:
            pass

        d = {'url': url, 'quality': quality}
        items.append(d)

    return items


# To load Fastplay Video stream url
def load_fastplay_video(url):
    soup = helper.get_soup_from_url(url)
    script = soup.find_all('script', type="text/javascript")
    # regex = re.compile('file:"(.*?),')
    regex = re.compile('file:(.*?)}')
    videofiles = re.findall(regex, str(script))
    items = []
    for video in videofiles:
        url = None
        quality = ''

        try:
            url = video.split('"')[1]
            quality = video.split('"')[3]
            if quality not in ['720p','360p','240p']:
                quality = ''

        except:
            pass

        d = {'url': url, 'quality': quality}
        items.append(d)
    return items
