import re
import helper as helper
from xbmcswift2 import xbmc
import urllib2
import base64


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


def load_fastplay_video(url_page):

    print (url_page)
    soup = helper.get_soup_from_url(url_page)

    #Getting host
    img_src = soup.find('img')['src']
    img_src_link = urllib2.urlparse.urlsplit(img_src)
    host = img_src_link.hostname

    items = []
    try :
        matches = re.findall('720p\|(.*?)\|', str(soup))
        if len(matches) > 0:
            url = 'http://{0}/{1}/v.mp4|Referer={2}'.format(host,matches[0],url_page)
            #url = 'http://' + host + '/' + matches[0] + '/' + 'v.mp4' + '|' + 'Referer=http://fastplay.to/
            d = {'url': url, 'quality': '720p', 'quality_icon': icon_720}
            items.append(d)

        matches = re.findall('360p\|(.*?)\|', str(soup))
        if len(matches) > 0:
            url = 'http://{0}/{1}/v.mp4|Referer={2}'.format(host,matches[0],url_page)
            #url = 'http://' + host + '/' + matches[0] + '/' + 'v.mp4'
            d = {'url': url, 'quality': '360p', 'quality_icon': icon_360}
            items.append(d)

        matches = re.findall('mp4\|(.*?)\|', str(soup))
        if len(matches) > 0:
            url = 'http://{0}/{1}/v.mp4|Referer={2}'.format(host,matches[0],url_page)
            #url = 'http://' + host + '/' + matches[0] + '/' + 'v.mp4'
            d = {'url': url, 'quality': '240p', 'quality_icon': icon_240}
            items.append(d)
    except:
        print ('Unaible to get video ligne from fastplay.to')

   #print items
    return items


def load_videohost2_video(url):
    #url = 'http://videohost2.com/playd.php?id=cj8xavpa64mvw0vsdrr5m2s6c'
    #print (url)
    print ('Url of video page {0}'.format(url))
    stream_url_path = None
    ext = None
    stream_url = ''

    soup = helper.get_soup_from_url(url)
    scripts = soup.find_all('script', type="text/javascript")


    for script in scripts:
        # Traitement base64 method
        #print (script)
        if 'atob' in str(script):
            print ('Traitement BASE64')
            regex = re.compile('atob\((.*?)\)')
            base64code = re.findall(regex, str(script))
            try :
                decoded_str = base64.b64decode(base64code[0].replace('"',''))
                regex = re.compile("src='(.*?)\?")
                try :
                    stream_url = re.findall(regex, str(decoded_str))[0]
                except:
                    print ('Src not found in base64 string')

            except:
                print ('Error decode base64 string')

        else:
            #Traitement hex method
            print ('Traitement HEX')
            regex = re.compile('=\[(.*?)];')
            scripts_bytecode = re.findall(regex, str(scripts))

            for script_bytecode in scripts_bytecode:
                for s in script_bytecode.split(','):
                    t = s.decode('string_escape').decode('string_escape')
                    print (t)
                    if 'https' in t:
                        stream_url_path = str(t).replace('"', '')

                    if '.' in t:
                        ext = str(t).replace('"', '')

            if (stream_url_path != None and ext != None):
                if '.mp' not in stream_url_path:
                    stream_url = stream_url_path + str(url.split('=')[-1]) + ext
                else:
                    stream_url = stream_url_path
                #d = {'url': stream_url, 'quality': '720p', 'quality_icon': icon_720}
                #items.append(d)
            else:
                print ('Imposible to make stream_url for videohost2')

    return stream_url