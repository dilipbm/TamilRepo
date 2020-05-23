from bs4 import BeautifulSoup
import re
import xbmc

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2


class MovieViewTypeEnum:
    ICON = 54
    LIST = 52
    LIST_INFO = 58
    LIST_INFO_2 = 66
    LIST_INFO_3 = 95
    THUMBS_INFO = 97
    WRAP_INFO = 53
    WRAP_3D = 588
    FANART = 583
    WALL = 69


ADDON_ID = "plugin.video.tamilstreamer"
ICON_NEXT = xbmc.translatePath(
    "special://home/addons/{0}/resources/images/next.png".format(ADDON_ID)
)
ICON_720 = xbmc.translatePath(
    "special://home/addons/{0}/resources/images/icon_720.png".format(ADDON_ID)
)
ICON_360 = xbmc.translatePath(
    "special://home/addons/{0}/resources/images/icon_360.png".format(ADDON_ID)
)
ICON_480 = xbmc.translatePath(
    "special://home/addons/{0}/resources/images/icon_360.png".format(ADDON_ID)
)
ICON_240 = xbmc.translatePath(
    "special://home/addons/{0}/resources/images/icon_240.png".format(ADDON_ID)
)
POSTER_PLACEHOLDER = xbmc.translatePath(
    "special://home/addons/{0}/resources/images/poster-placeholder.png".format(ADDON_ID)
)
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"


def color_movie_name(movie_name):
    movie_name = re.sub(
        r"\sHDRip|\sHD", " [B][COLOR green] HD [/COLOR][/B]", movie_name
    )
    movie_name = re.sub(
        r"\sCAM", " [B][COLOR cornflowerblue] CAM [/COLOR][/B]", movie_name
    )
    movie_name = re.sub(
        r"\sDVDScr", " [B][COLOR skyblue] DVDScr [/COLOR][/B]", movie_name
    )
    movie_name = re.sub(
        r"\sDVDRip", " [B][COLOR skyblue] DVDRip [/COLOR][/B]", movie_name
    )

    return movie_name


def encode_url(url):
    return url.replace("/", "____")


def decode_url(url):
    return url.replace("____", "/")


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
        opener.addheaders = [("User-agent", "Mozilla/5.0")]
        r = opener.open(req)
        html = r.read()

    except urllib2.HTTPError as e:
        html = e.fp.read()

    try:
        soup = BeautifulSoup(html, "html.parser")
        # rint type(html)
    except:
        html = html.replace(
            '</bo"+"dy>', "</body>"
        )  # Correction html tag only for mac/android version for tamilyogi site
        html = html.replace(
            '</ht"+"ml', "</html"
        )  # Correction html tag only for mac/android version for tamilyogi site
        soup = BeautifulSoup(html, "html.parser")

    return soup


def get_soup_from_text(text):
    soup = BeautifulSoup(text, "html.parser")

    return soup


# To remove duplicates in list
def remove_duplicates(List):
    y = len(List) - 1
    while y > 0:
        if List.count(List[y]) > 1:
            List.remove(List[y])
        y -= 1
    return List


# def thumbnailView():
#  xbmc.executebuiltin('Container.SetViewMode(500)')


def movie_name_resolver(name):
    name = name.replace(u"\u2019", u"'").encode(
        "ascii", "ignore"
    )  # to resolu sigle code encode probleme
    name = name.replace(u"\u2013", u"'").encode(
        "ascii", "ignore"
    )  # to resolu sigle code encode probleme
    name = name.replace("Tamil Full Movie Watch Online", "")
    name = name.replace("Tamil Movie Watch Online", "")
    name = name.replace("Tamil Movie Online", "")
    name = name.replace("Telugu Movie Online", "")
    name = name.replace("Tamil Dubbed Movie", "")
    name = name.replace("Watch Online", "")
    name = name.replace("Watch ", "")
    name = name.replace("Movie Watch Online", "")
    name = name.replace("720p", "")
    name = name.strip()
    return name


class JWplayer(object):
    def __init__(self, url_player):
        self.url = url_player
        self.html = self._get_html(self.url)
        if "p,a,c,k,e,d" in self.html:
            self.beautified = self._beautify(self.html)

    def _get_html(self, url):
        proxy_handler = urllib2.ProxyHandler({})
        opener = urllib2.build_opener(proxy_handler)
        try:
            req = urllib2.Request(url)
            opener.addheaders = [("User-agent", "Mozilla/5.0")]
            r = opener.open(req)
            html = r.read()

        except urllib2.HTTPError as e:
            html = e.fp.read()

        return html

    def _beautify(self, html):
        soup = get_soup_from_text(html)
        pattern = re.compile("eval(.*?)")
        f = soup.find_all(text=pattern)

        for e in f:
            if "p,a,c,k,e,d" in str(e):
                encrypted = str(e).rstrip()

            else:
                continue

        # encrypted = r'''eval(function(p,a,c,k,e,d){while(c--)if(k[c])p=p.replace(new RegExp('\\b'+c.toString(a)+'\\b','g'),k[c]);return p}('7("2i").2h({2g:[{n:"6://c.3.2/2f/v.m",l:"2e","2d":"j"},{n:"6://c.3.2/2c/v.m",l:"2b"}],2a:"6://c.3.2/i/29/28/e.27",26:"25",24:"23%",22:"21",20:"16:9",1z:"k",1y:"k",1x:"j",1w:"1v",1u:[],1t:{1s:\'#1r\',1q:15,1p:"1o",1n:0},1m:"1l",1k:"3.2 - 1j 1i 1h",1g:"6://3.2"});1f 8,b;7().1e(4(x){f(5>0&&x.1d>=5&&b!=1){b=1;$(\'a.1c\').1b(\'1a\')}});7().19(4(x){h(x)});7().18(4(){$(\'a.g\').17()});4 h(x){$(\'a.g\').14();f(8)13;8=1;$.12(\'6://3.2/11?10=z&y=e&w=u-t-s-r-q\',4(d){$(\'#p\').o(d)})}',36,91,'||to|fastplay|function||http|jwplayer|vvplay||div|vvad|www32|data|tw9od28s1tqh|if|video_ad|doPlay||true|none|label|mp4|file|html|fviews|6ea4b88148dda140ee636feb8dbe2833|1510436630|193|78|53124||hash||file_code|view|op|dl|get|return|hide|||show|onComplete|onPlay|slow|fadeIn|video_ad_fadein|position|onTime|var|aboutlink|Hosting|Video|HD|abouttext|beelden|skin|backgroundOpacity|Verdana|fontFamily|fontSize|FFFFFF|color|captions|tracks|start|startparam|androidhls|preload|primary|aspectratio|450|height|100|width|8216|duration|jpg|00010|01|image|720p|2tdvyi34mqjtgz575oulryw4nvlmw2t4icjuwbm4t6ndzhmdqhlzi22pz36a|default|360p|2tdvyi34mqjtgz575oulryw4nvlmw2t4icjuwbm4tgndzhmdqhlslnagehza|sources|setup|vplayer'.split('|')))'''
        # encrypted = r'''eval(function(p,a,c,k,e,d){e=function(c){return c};if(!''.replace(/^/,String)){while(c--)d[c]=k[c]||c;k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1;};while(c--)if(k[c])p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c]);return p;}('5 11=17;5 12=["/3/2/1/0/13.4","/3/2/1/0/15.4","/3/2/1/0/14.4","/3/2/1/0/7.4","/3/2/1/0/6.4","/3/2/1/0/8.4","/3/2/1/0/10.4","/3/2/1/0/9.4","/3/2/1/0/23.4","/3/2/1/0/22.4","/3/2/1/0/24.4","/3/2/1/0/26.4","/3/2/1/0/25.4","/3/2/1/0/18.4","/3/2/1/0/16.4","/3/2/1/0/19.4","/3/2/1/0/21.4"];5 20=0;',10,27,'40769|54|Images|Files|png|var|imanhua_005_140430179|imanhua_004_140430179|imanhua_006_140430226|imanhua_008_140430242|imanhua_007_140430226|len|pic|imanhua_001_140429664|imanhua_003_140430117|imanhua_002_140430070|imanhua_015_140430414||imanhua_014_140430382|imanhua_016_140430414|sid|imanhua_017_140430429|imanhua_010_140430289|imanhua_009_140430242|imanhua_011_140430367|imanhua_013_140430382|imanhua_012_140430367'.split('|'),0,{}))'''

        encrypted = encrypted.split("}(")[1][:-1]

        decrypted = eval("JWplayer.unpack(" + encrypted)
        # print (decrypted)
        return decrypted

    @staticmethod
    def baseN(num, b, numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
        return ((num == 0) and numerals[0]) or (
            JWplayer.baseN(num // b, b, numerals).lstrip(numerals[0])
            + numerals[num % b]
        )

    @staticmethod
    def unpack(p, a, c, k, e=None, d=None):
        while c:
            c -= 1
            if k[c]:
                p = re.sub("\\b" + JWplayer.baseN(c, a) + "\\b", k[c], p)
        return p

    def sources(self):
        pattern = re.compile('file\s*:\s*"([^"]+)",label:"(.*?)"')
        sources = re.findall(pattern, self.beautified)
        return sources


# url = 'http://fastplay.to/embed-vmbkhvs0n6vr.html'
# jwp = JWplayer(url)
# sources = jwp.sources()
