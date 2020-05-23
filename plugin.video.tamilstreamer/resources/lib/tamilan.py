from bs4 import BeautifulSoup
import requests
import re

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

import xbmcgui

from resources.lib import utils
from resources.lib import stream_resolver
from resources.lib.utils import ADDON_ID, ICON_NEXT, ICON_240, ICON_360, ICON_720


class Tamilan(object):
    def __init__(self):
        self.sess = requests.session()
        self.sess.headers.update({"User-Agent": utils.USER_AGENT})

    def _decode_html(self, encoded_html):
        """Decode encoded HTML"""

        soup = BeautifulSoup(encoded_html, "html.parser")

        js = soup.find("script").text
        pattern_script = re.compile(r"(\[.*?\])")
        try:
            encoded_html = re.findall(pattern_script, js)[0]
            encoded_html_list = eval(encoded_html)
        except IndexError:
            encoded_html_list = []
        try:
            sub_val = int(re.findall(r"-\s+(\d+)", js)[0])
        except IndexError:
            sub_val = None

        if sub_val and len(encoded_html_list) > 0:
            decoded_html = "".join(
                map(chr, [encoded_val - sub_val for encoded_val in encoded_html_list])
            )
            return decoded_html
        else:
            return None

    def _get_video_id(self, url):
        response = self.sess.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        input_ = soup.find("input", {"type": "hidden"})
        if input_:
            return input_.get("value")
        else:
            return None

    def _get_video_action_url(self, url):
        action_url = None
        response = self.sess.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        movie_form = soup.find("form", {"id": "movie-form"})
        if not movie_form:
            for mva in soup.find_all("form"):
                action_url = mva.get("action")
                if action_url and action_url.endswith("check-source/"):
                    break
        if movie_form:
            action_url = movie_form.get("action")

        return action_url

    def _get_sources(self, video_id, action_url):

        if video_id == "" or action_url == "":
            raise ValueError("video ID or action url missing")

        if not action_url.startswith("http"):
            action_url = "https:{}".format(action_url)
        response = self.sess.post(action_url, data={"id": video_id})

        # If not encoded
        if "<title>" not in response.text:
            html = self._decode_html(response.text)
        else:
            html = response.text

        soup = BeautifulSoup(html, "html.parser")
        video_src = soup.find("iframe").get("src")
        if "vidmojo.net" in video_src:
            return stream_resolver.load_vidmojo(video_src, action_url)

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
        img = ""
        next_page = {}

        pDialog = xbmcgui.DialogProgress()
        pDialog.create("Loading", "Loading movies...")

        if "search" in url:
            s = xbmcgui.Dialog().input(
                "Search for movie name", type=xbmcgui.INPUT_ALPHANUM
            )
            if s == "":
                return []

            url = "https://tamilian.net/?s={}".format(s)

        response = self.sess.get(url)
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        movie_preview = soup.find_all("div", {"class": "movie-preview"})
        progress = 0
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

        try:
            next_page_url = soup.find("a", {"class": "loadnavi"}).get("href")
        except:
            next_page_url = None

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
        video_action_url = self._get_video_action_url(url)
        stream_urls = self._get_sources(video_id, video_action_url)
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
