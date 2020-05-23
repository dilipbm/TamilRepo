from bs4 import BeautifulSoup
import requests
import re

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

import xbmcgui

from resources.lib import utils
from resources.lib.utils import ADDON_ID, ICON_NEXT, ICON_240, ICON_360, ICON_720


class Tamilan(object):
    def __init__(self):
        self.sess = requests.session()
        self.sess.headers.update({"User-Agent": utils.USER_AGENT})

    def _get_video_id(self, url):
        video_id = None
        response = self.sess.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        movie_form = soup.find("form", {"id": "movie-form"})

        if movie_form:
            video_id = movie_form.find("input").get("value")

        return video_id or None

    def _get_sources(self, video_id):
        sources = []
        url = "https://mguire.com/verifying-source/"
        response = self.sess.post(url, data={"id": video_id})
        soup = BeautifulSoup(response.text, "html.parser")

        js = soup.find("script").text
        pattern_script = re.compile(r"(\[.*?\])")
        try:
            encoded_html = re.findall(pattern_script, js)[0]
            encoded_html_list = eval(encoded_html)
        except KeyError:
            encoded_html_list = []

        try:
            sub_val = int(re.findall(r"-\s+(\d+)", js)[0])
        except KeyError:
            sub_val = None
        if sub_val and len(encoded_html_list) > 0:
            decoded_html = "".join(
                map(chr, [encoded_val - sub_val for encoded_val in encoded_html_list])
            )
            soup = BeautifulSoup(decoded_html, "html.parser")
            video_src = soup.find("iframe").get("src")
            self.sess.headers.update(
                {"referer": "https://mguire.com/verifying-source/"}
            )
            response = self.sess.get(video_src)
            del self.sess.headers["referer"]

            pattern = re.compile(r"eval(.*?)")
            soup = BeautifulSoup(response.text, "html.parser")
            find_eval = soup.find_all(text=pattern)
            for e in find_eval:
                if "p,a,c,k,e,d" in str(e):
                    try:
                        encrypted = str(e).rstrip().split("}(")[1][:-1]
                    except:
                        encrypted = None

                else:
                    continue

            decrypted = eval("Tamilan.unpack(" + encrypted)

            try:
                pattern_source = re.compile(r'sources.*src:.?"(https://.*?)"')
                source = re.findall(pattern_source, decrypted)
                sources.append(
                    {
                        "url": source[0],
                        "quality": "720p",
                        "quality_icon": eval("ICON_" + "720"),
                    }
                )
            except KeyError:
                source = None

        return sources

    @staticmethod
    def baseN(num, b, numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
        return ((num == 0) and numerals[0]) or (
            Tamilan.baseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b]
        )

    @staticmethod
    def unpack(p, a, c, k, e=None, d=None):
        while c:
            c -= 1
            if k[c]:
                p = re.sub("\\b" + Tamilan.baseN(c, a) + "\\b", k[c], p)
        return p

    def get_sections(self):
        """
        get all section for tamilan website
        :return:
        """
        sections = [
            {"name": "Home", "url": "https://tamilian.net/tamil-movies-online-free/"},
            {"name": "Action", "url": "https://tamilian.net/action/"},
            {"name": "Adventure", "url": "https://tamilian.net/adventure/"},
            {"name": "Comedy", "url": "https://tamilian.net/comedy/"},
            {"name": "Crime", "url": "https://tamilian.net/crime/"},
            {"name": "Drama", "url": "https://tamilian.net/drama/"},
            {"name": "Family", "url": "https://tamilian.net/family/"},
            {"name": "Fantasy", "url": "https://tamilian.net/fantasy/"},
            {"name": "History", "url": "https://tamilian.net/history/"},
            {"name": "Horror", "url": "https://tamilian.net/horror/"},
            {"name": "Sci-Fi", "url": "https://tamilian.net/sci-fi/"},
            {"name": "Thriller", "url": "https://tamilian.net/thriller/"},
            {"name": "Romance", "url": "https://tamilian.net/romance/"},
            {"name": "Search", "url": "search"},
        ]

        return [section for section in sections if section["name"] and section["url"]]

    def get_movies(self, url):
        """
        get all movies from given section url
        :param url:
        :return:
        """
        movies = []
        added_items = []
        img = ""
        next_page = {}
        infos = {}

        pDialog = xbmcgui.DialogProgress()
        pDialog.create("Loading", "Loading movies...")

        if "search" in url:
            s = xbmcgui.Dialog().input(
                "Search for movie name", type=xbmcgui.INPUT_ALPHANUM
            )
            if s == "":
                return []

            url = "https://tamilian.net/?s={}".format(s)

        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        progress = 0
        movie_preview = soup.find_all("div", {"class": "movie-preview"})
        for movie in movie_preview:
            title_span = movie.find("span", {"class": "movie-title"})
            title = title_span.find("a").text
            title = utils.movie_name_resolver(title)
            url = title_span.find("a").get("href")

            release_span = movie.find("span", {"class": "movie-release"})
            if release_span:
                title = "{} - {}".format(title, release_span.text.rstrip())

            img = movie.find("img").get("src")
            if not img.startswith("http"):
                try:
                    img = "https:{}".format(img)
                except UnicodeEncodeError:
                    img = utils.POSTER_PLACEHOLDER

            movies.append(
                {"name": title, "url": url, "image": img, "infos": {"title": title}}
            )
            progress += 100 / len(movie_preview)
            pDialog.update(progress)

        next_page_url = soup.find("a", {"class": "loadnavi"}).get("href")
        print("##### NEXT PAGE")
        print(next_page_url)
        print(soup.find("a", {"class": "loadnavi"}))
        if next_page_url:
            next_page = {
                "name": "Next Page",
                "image": ICON_NEXT,
                "infos": {},
                "url": next_page_url,
            }
            movies.append(next_page)

        return [movie for movie in movies if movie["name"] and movie["url"]]

    def get_stream_urls(self, movie_name, url):
        """
        get stream urls from movie page url.
        :param movie_name:
        :param url:
        :return:
        """
        video_id = self._get_video_id(url)
        stream_urls = self._get_sources(video_id)
        print("##### STREAM")
        print(stream_urls)
        return [
            {
                "name": movie_name,
                "quality": stream_url["quality"],
                "quality_icon": stream_url["quality_icon"],
                "url": stream_url["url"],
            }
            for stream_url in stream_urls
            if stream_url["url"]
        ]


if __name__ == "__main__":
    t = Tamilan()
    video_id = t._get_video_id("https://tamilian.net/walter/")
    source = t._get_source(video_id)
