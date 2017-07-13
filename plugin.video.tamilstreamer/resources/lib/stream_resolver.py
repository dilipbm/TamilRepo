import re
import helper as helper
from xbmcswift2 import xbmc
import urllib2


addon_id = 'plugin.video.tamilstreamer'
icon_720 = xbmc.translatePath('special://home/addons/{0}/resources/images/icon_720.png'.format(addon_id))
icon_360 = xbmc.translatePath('special://home/addons/{0}/resources/images/icon_360.png'.format(addon_id))
icon_240 = xbmc.translatePath('special://home/addons/{0}/resources/images/icon_240.png'.format(addon_id))

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
        quality = ''

        try:
            url = video.split('"')[1]
            quality = video.split('"')[3]
            if quality == '720p':
                quality_icon = icon_720

            elif quality == '360p':
                quality_icon = icon_360

            elif quality == '240p':
                quality_icon = icon_240

            else:
                quality = ''
                quality_icon = ''
        except:
            pass

        d = {'url': url, 'quality': quality, 'quality_icon': quality_icon}
        items.append(d)

    return items


# To load Fastplay Video stream url
# def load_fastplay_video(url):
#     soup = helper.get_soup_from_url(url)
#     script = soup.find_all('script', type="text/javascript")
#     # regex = re.compile('file:"(.*?),')
#     regex = re.compile('file:(.*?)}')
#     videofiles = re.findall(regex, str(script))
#     items = []
#     for video in videofiles:
#         url = None
#         quality = ''
#
#         try:
#             url = video.split('"')[1]
#             quality = video.split('"')[3]
#             if quality == '720p':
#                 quality_icon = icon_720
#
#             elif quality == '360p':
#                 quality_icon = icon_360
#
#             elif quality == '240p':
#                 quality_icon = icon_240
#
#             else:
#                 quality = ''
#                 quality_icon = ''
#
#         except:
#             pass
#
#         d = {'url': url, 'quality': quality, 'quality_icon': quality_icon}
#         items.append(d)
#     return items


def load_fastplay_video(url):
    soup = helper.get_soup_from_url(url)

    #Getting host
    img_src = soup.find('img')['src']
    img_src_link = urllib2.urlparse.urlsplit(img_src)
    host = img_src_link.hostname

    items = []
    try :
        matches = re.findall('720p\|(.*?)\|', str(soup))
        if len(matches) > 0:
            url = 'http://' + host + '/' + matches[0] + '/' + 'v.mp4'
            d = {'url': url, 'quality': '720p', 'quality_icon': icon_720}
            items.append(d)

        matches = re.findall('360p\|(.*?)\|', str(soup))
        if len(matches) > 0:
            url = 'http://' + host + '/' + matches[0] + '/' + 'v.mp4'
            d = {'url': url, 'quality': '360p', 'quality_icon': icon_360}
            items.append(d)
    except:
        print ('Unaible to get video ligne from fastplay.to')

    print items
    return items