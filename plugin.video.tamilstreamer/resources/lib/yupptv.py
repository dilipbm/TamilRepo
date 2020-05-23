import requests
import re
import os
from bs4 import BeautifulSoup

import xbmcplugin
import xbmcgui
import xbmcvfs
import xbmcaddon
import xbmc


try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


try:
    import cPickle as pickle
except ImportError:
    import pickle


BASE_URL = "https://www.yupptv.com/"
TV_MAPPING = [
    {
        "name": "Sun TV",
        "slug": "sun-tv-hd",
        "image": "https://d229kpbsb5jevy.cloudfront.net/tv/150/150/bnw/sun-HD-white.png",
    },
    {
        "name": "KTV",
        "slug": "ktv-hd",
        "image": "https://d229kpbsb5jevy.cloudfront.net/tv/150/150/bnw/ktv-HD-white.png",
    },
    {
        "name": "Vijay TV",
        "slug": "star-vijay",
        "image": "https://d229kpbsb5jevy.cloudfront.net/tv/150/150/bnw/star-vijay-white.png",
    },
    {
        "name": "Color TV",
        "slug": "colors-tamil",
        "image": "https://d229kpbsb5jevy.cloudfront.net/tv/150/150/bnw/Colors-Tamil-white.png",
    },
    {
        "name": "Adithya",
        "slug": "adithya-tv",
        "image": "https://d229kpbsb5jevy.cloudfront.net/tv/150/150/bnw/adithya-tv-white.png",
    },
    {
        "name": "IBC",
        "slug": "ibc-tamil",
        "image": "https://d229kpbsb5jevy.cloudfront.net/tv/150/150/bnw/IBC-Tamil-new1-white.png",
    },
    {
        "name": "KBO",
        "slug": "kbo",
        "image": "https://d229kpbsb5jevy.cloudfront.net/tv/150/150/bnw/kbo-white.png",
    },
    # {
    #     "name": "Surya TV",
    #     "slug": "surya-tv",
    #     "image": "https://d229kpbsb5jevy.cloudfront.net/tv/150/150/bnw/surya-tv-white.png",
    # },
    # {
    #     "name": "Surya Movie",
    #     "slug": "surya-movie",
    #     "image": "https://d229kpbsb5jevy.cloudfront.net/tv/150/150/bnw/surya-movies-white.png",
    # },
    {
        "name": "Sirippoli TV",
        "slug": "sirippoli-tv",
        "image": "https://d229kpbsb5jevy.cloudfront.net/tv/150/150/bnw/sirippoli-tv-white.png",
    },
    # {
    #    "name": "Surya TV HD",
    #    "slug": "surya-tv-hd-",
    #    "image": "https://d229kpbsb5jevy.cloudfront.net/tv/150/150/bnw/Surya_TV_HD_white.png",
    # },
]


class Yupptv(object):
    def __init__(self, plugin):
        if "yupptv" in plugin.path:
            self.box_id = None
            self.storage_name = "YTP_COOKIES"
            self.username = xbmcplugin.getSetting(plugin.handle, "username")
            self.password = xbmcplugin.getSetting(plugin.handle, "password")

            if self.username == "" or self.password == "":
                xbmcgui.Dialog().ok(
                    "YuppTV warning",
                    "You have to use your Yupptv account to connect. Goto addons setting",
                )

            self.sess = requests.session()
            self.sess.headers.update(
                {
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
                }
            )

            stored_cookies = self.get_data_from_storage(self.storage_name)
            print("#### SORED")
            print(stored_cookies)
            if stored_cookies:
                self.sess.cookies = stored_cookies

            if not self.sess.cookies.get("BoxId"):
                self.login()
        else:
            pass

    @property
    def hasCredentiels(self):
        if self.username == "" or self.password == "":
            return False
        else:
            return True

    def set_data_to_storage(self, name, data):
        data_path = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo("profile"))
        storage = os.path.join(data_path, "{}.pkl".format(name))
        pickle.dump(data, open(storage, "wb"))

    def get_data_from_storage(self, name):
        data_path = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo("profile"))
        storage = os.path.join(data_path, "{}.pkl".format(name))
        return pickle.load(open(storage, "rb"))

    def login(self):
        print("######## YUPP LOGIN")
        url = urljoin(BASE_URL, "auth/validateSignin")
        data = {"user": self.username, "password": self.password}
        response = self.sess.post(url, data)
        if response.status_code == 200:
            respose_data = response.json().get("Response")
            login_status = respose_data.get("status")
            if login_status == "2":
                print("Session already existe, has to logout")
                box_id = response.json().get("tempBoxid")
                logout_success = self.logout(box_id)
                if logout_success:
                    print("###### RETRY LOGIN")
                    response = self.sess.post(url, data)
                    if (
                        response.status_code == 200
                        and response.json().get("Response").get("status") == "1"
                    ):

                        self.set_data_to_storage(self.storage_name, self.sess.cookies)

                        print("LOGIN SUCCESS")
                        xbmcgui.Dialog().notification(
                            "YuppTV login status", "Login success"
                        )
                        return True
            elif login_status == "1":
                xbmcgui.Dialog().notification("YuppTV login status", "Login success")
                print("LOGIN SUCCESS")
                self.set_data_to_storage(self.storage_name, self.sess.cookies)
                return True
            else:
                pass
        xbmcgui.Dialog().notification("YuppTV login status", "Login failed")
        return False

    def logout(self, box_id):
        print("Try to logout")
        url = urljoin(BASE_URL, "auth/confirmLogout")
        payload = {"boxId": box_id}
        response = self.sess.get(url, params=payload)
        if response.status_code == 200:
            print("Logout success")
            xbmcgui.Dialog().notification("YuppTV login status", "Logout success")
            return True

        return False

    def find_stream_url(self, page_url):
        # print("#### FIND STREAM URL")
        # print(page_url)

        response = self.sess.get(page_url)
        if response.status_code == 200:
            pattern = re.compile(r'streamUrl.*src:\s?"(.*)"')
            urls = re.findall(pattern, response.text)
            if len(urls) > 0:
                if "preview" in urls[0]:
                    xbmcgui.Dialog().notification(
                        "Information",
                        "This is a preview. We are trying to reconnect with your credentiels",
                    )
                    self.login()
                    new_response = self.sess.get(page_url)
                    urls = re.findall(pattern, new_response.text)

                return "{}|User-Agent='{}'".format(
                    urls[0], self.sess.headers["User-Agent"]
                )

        return None

    def get_sections(self):
        """
        get all section for tamilyogi website
        :return:
        """
        sections = [
            {"name": "Live TV", "url": "live",},
            {"name": "Catch up", "url": "catchup",},
            {"name": "Reconnect", "url": "reconnect",},
        ]

        return [section for section in sections if section["name"] and section["url"]]

    def get_channels(self, url):
        """
        get all programme by channel from given section url
        :param url:
        :return:
        """
        if url == "live":
            items = [
                {
                    "name": channel_item["name"],
                    "url": "https://www.yupptv.com/channels/{}/live".format(
                        channel_item["slug"]
                    ),
                    "image": channel_item["image"],
                }
                for channel_item in TV_MAPPING
            ]
        elif url == "catchup":
            items = [
                {
                    "name": channel_item["name"],
                    "url": "https://www.yupptv.com/channels/catchupPartial/{}".format(
                        channel_item["slug"]
                    ),
                    "image": channel_item["image"],
                }
                for channel_item in TV_MAPPING
            ]

        sorted_items = sorted(items, key=lambda k: k["name"])
        return sorted_items

    def get_programmes(self, url):
        pDialog = xbmcgui.DialogProgress()
        pDialog.create("Loading", "Loading elements...")
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        programmes = []
        a_tags = soup.find_all("a")
        progress = 0
        for item in a_tags:
            data = {}
            data["url"] = item.get("href") or ""
            title = item.find("div", {"class": "show-name"}).text
            time = item.find("span", {"class": "show-time"}).text
            data["name"] = "{} | {}".format(title, time)
            data["image"] = (
                item.find("img").get("data-src")
                or "https://d3hprka3kr08q2.cloudfront.net/yupptv/yupptv_new/Web/Content/images/default-live-catchup.jpg"
            )
            data["infos"] = {}

            programmes.append(data)
            progress += 100 / len(a_tags)
            pDialog.update(progress)

        print(programmes)
        return programmes

    def get_episodes(self, url):
        """
        get all episodes from given url
        :param url:
        :return:
        """
        episodes = []

        episode = dict(
            name="Play", url="", prog_name="suntvlive", infos={"title": "Sun TV"}
        )
        episodes.append(episode)

        return episodes

    def get_stream_urls(self, movie_name, url):
        """
        get stream urls from movie page url.
        :param movie_name:
        :param url:
        :return:
        """

        stream_urls = []
        self.find_stream_url(url)
        return [{"name": "Test", "quality": "", "quality_icon": "", "url": ""}]
