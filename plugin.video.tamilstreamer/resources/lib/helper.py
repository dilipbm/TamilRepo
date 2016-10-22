
import urllib, urllib2
from bs4 import BeautifulSoup

def get_soup_from_url(url):
    """
    :param url:
    :return:
    Help fonction that return a soup object from a url
    """
    proxy_handler = urllib2.ProxyHandler({})
    opener = urllib2.build_opener(proxy_handler)
    try:
        req = urllib2.Request(url)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        r = opener.open(req)
        html = r.read()

    except urllib2.HTTPError, e:
        html = e.fp.read()


    try:
        soup = BeautifulSoup(html, 'html.parser')
        print type(html)
    except:
        html = html.replace('</bo"+"dy>', '</body>') # Correction html tag only for mac/android version for tamilyogi site
        html = html.replace ('</ht"+"ml', '</html') # Correction html tag only for mac/android version for tamilyogi site
        soup = BeautifulSoup(html, 'html.parser')

    return soup

#To remove duplicates in list
def remove_duplicates(List):
    y = len(List) - 1
    while y > 0:
        if List.count(List[y]) > 1:
            List.remove(List[y])
        y -= 1
    return List

#def thumbnailView():
#  xbmc.executebuiltin('Container.SetViewMode(500)')

def movie_name_resolver(name):
    name = name.replace(u'\u2019', u'\'').encode('ascii', 'ignore') # to resolu sigle code encode probleme
    name = name.replace('Tamil Full Movie Watch Online', '')
    name = name.replace('Tamil Movie Watch Online', '')
    name = name.replace('Tamil Dubbed Movie', '')
    name = name.replace('Watch Online', '')
    name = name.replace('720p', '')
    name = name.strip()
    return name