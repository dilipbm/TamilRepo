import re
import urllib2
import base64
import xbmc

from resources.lib import helper

addon_id = 'plugin.video.tamilstreamer'
icon_720 = xbmc.translatePath('special://home/addons/{0}/resources/images/icon_720.png'.format(addon_id))
icon_360 = xbmc.translatePath('special://home/addons/{0}/resources/images/icon_360.png'.format(addon_id))
icon_480 = xbmc.translatePath('special://home/addons/{0}/resources/images/icon_360.png'.format(addon_id))
icon_240 = xbmc.translatePath('special://home/addons/{0}/resources/images/icon_240.png'.format(addon_id))


#def load_vidmad_video(url):
#    soup = helper.get_soup_from_url(url)
#    script = soup.find_all('script', type="text/javascript")
#    regex = re.compile('file:(.*?)}')
#    print('regex', regex)
#    videofiles = re.findall(regex, str(script))
#    items = []
#    print ('videosfiles', videofiles)
#    for video in videofiles:
#        url = None
#        quality = ''
#
#        try:
#            url = video.split('"')[1]
#            quality = video.split('"')[3]
#            if quality == '720p':
#                quality_icon = icon_720
#
#            elif quality == '360p':
#                quality_icon = icon_360
#
#            elif quality == '240p':
#                quality_icon = icon_240
#
#            else:
#                quality = ''
#                quality_icon = ''
#        except:
#            pass
#
#        d = {'url': url, 'quality': quality, 'quality_icon': quality_icon}
#        items.append(d)
#
#    return items


def load_dailymotion_video(url):
    video_id = url.split('/')[-1]
    return 'plugin://plugin.video.dailymotion_com/?url={}&mode=playVideo'.format(video_id)

def load_youtube_video(url):
    video_id = url.split('/')[-1].split('?')[0]
    return 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' %video_id


def load_tamiltvtube_videos(url):
    soup = helper.get_soup_from_url(url)
    #print(soup.text)

    if 'p,a,c,k,e,d' in soup.text:
        jwp = helper.JWplayer(url)
        sources = jwp.sources()

        items = [
                {'url': source[0] + '|Referer=' + url, 
                'quality': source[1], 
                'quality_icon': eval('icon_' + source[1].replace('p',''))} for source in sources]

    else:
        links = re.findall(r'file:"(http|https:.*?mp4)"', soup.text)
        qualities = re.findall(r'label:"(\d*p)"', soup.text)
        items = []
        for l, q in zip(links, qualities):
            d = {   
                    'url': l, 
                    'quality': q, 
                    'quality_icon': eval('icon_' + q.replace('p',''))
                }
            items.append(d)

    return items


# Load Vidorg
def load_vidorg_videos(url):
    soup = helper.get_soup_from_url(url)
    links = re.findall(r'file:"(http:.*?)"', soup.text)
    qualities = re.findall(r'label:"(\d*p)"', soup.text)
    items = []
    for l, q in zip(links, qualities):
        d = {   
                'url': l, 
                'quality': q, 
                'quality_icon': eval('icon_' + q.replace('p',''))
            }
        items.append(d)

    return items

# To load Vidmad Video stream url
def load_vidmad_video(url):
    soup = helper.get_soup_from_url(url)

    if 'p,a,c,k,e,d' in soup.text:
        jwp = helper.JWplayer(url)
        sources = jwp.sources()

        items = [
                {'url': source[0] + '|Referer=' + url, 
                'quality': source[1], 
                'quality_icon': eval('icon_' + source[1].replace('p',''))} for source in sources]

    else:
        links = re.findall(r'file:"(http|https:.*?mp4)"', soup.text)
        qualities = re.findall(r'label:"(\d*p)"', soup.text)
        items = []
        for l, q in zip(links, qualities):
            d = {   
                    'url': l + '|Referer=' + url_page, 
                    'quality': q, 
                    'quality_icon': eval('icon_' + q.replace('p',''))
                }
            items.append(d)

    return items


def load_fastplay_video(url_page):
    soup = helper.get_soup_from_url(url_page)

    if 'p,a,c,k,e,d' in soup.text:
        jwp = helper.JWplayer(url_page)
        sources = jwp.sources()

        items = [
                {'url': source[0] + '|Referer=' + url_page, 
                'quality': source[1], 
                'quality_icon': eval('icon_' + source[1].replace('p',''))} for source in sources]

    
    else:
        links = re.findall(r'file:"(http|https:.*?mp4)"', soup.text)
        qualities = re.findall(r'label:"(\d*p)"', soup.text)
        items = []
        for l, q in zip(links, qualities):
            d = {   
                    'url': l + '|Referer=' + url_page, 
                    'quality': q, 
                    'quality_icon': eval('icon_' + q.replace('p',''))
                }
            items.append(d)

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