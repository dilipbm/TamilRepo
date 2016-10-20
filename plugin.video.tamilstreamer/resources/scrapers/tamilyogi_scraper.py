from ..lib import helper, stream_resolver
import urllib, urllib2


def movie_loader(url):
    """
    	Load TamilYogi main page
    	:url - tamilyogi
    	:title, image, movie page and next page url of main page.
    	"""

    movies = []
    added = []
    nextpage = ''
    img = ''
    soup = helper.get_soup_from_url(url)

    for a in soup.find_all('a'):
        title = a.get('title')
        try:
            nextpagetag = a.get('class')
            if 'next' in nextpagetag:
                next_page_url = a.get('href')
                next_page = {'name': 'Next Page',
                             'image': '',
                             'url': next_page_url}
        except:
            pass

        try:
            img = a.find('img')['src']
        except:
            pass

        if (title is not None) and (title != 'Tamil Movie Online') and img != '':
            try:
                if title not in added:
                    d = {'name': helper.movie_name_resolver(title),
                         'image': img,
                         'url': a.get('href')
                         }
                    movies.append(d)
                    added.append(title)
            except:
                pass
    movies.append(next_page)
    return movies


def get_stream_url(movie_page_url):
    soup = helper.get_soup_from_url(movie_page_url)
    l = soup.find_all('iframe')
    for iframe in l:
        print 'in get_Stream_url'

        src = iframe.get('src')
        link = urllib2.urlparse.urlsplit(src)
        host = link.hostname
        host = host.replace('www.', '')
        host = host.replace('.com', '')
        host = host.replace('.tv', '')
        host = host.replace('.net', '')
        host = host.replace('.cc', '')
        host = host.replace('.sx', '')
        hostName = host.capitalize()
        # print "HostName = " + hostName

        print src

        if hostName == 'Vidmad':
            videofile = stream_resolver.load_vidmad_video(src)

        elif hostName == 'vidmad':
            videofile = stream_resolver.load_vidmad_video(src)

        elif hostName == 'Fastplay':
            videofile = stream_resolver.load_fastplay_video(src)

        elif hostName == 'fastplay':
            videofile = stream_resolver.load_fastplay_video(src)

        else:
            # print 'Host ingored!!'
            videofile = None
            pass

    return videofile
