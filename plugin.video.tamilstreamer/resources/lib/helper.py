
import urllib, urllib2
from bs4 import BeautifulSoup

def get_soup_from_url(url):
  """
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
    pass

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
    name = name.replace('Tamil Full Movie Watch Online', '')
    name = name.replace('Tamil Movie Watch Online', '')
    name = name.replace('Tamil Dubbed Movie', '')
    name = name.replace('Watch Online', '')
    name = name.strip()
    return name