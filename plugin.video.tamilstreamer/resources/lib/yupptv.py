import requests
import re
from bs4 import BeautifulSoup

import xbmcplugin

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
    def __init__(self, plugin, storage_file):
        self.username = xbmcplugin.getSetting(plugin.handle, "username")
        self.password = xbmcplugin.getSetting(plugin.handle, "password")
        self.storage_file = storage_file
        self.sess = requests.session()
        self.sess.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
            }
        )

        try:
            storage_file_obj = open(self.storage_file, "rb")
            self.sess.cookies = pickle.load(storage_file_obj)
            storage_file_obj.close()
        except IOError:
            pass

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
                        storage_file_obj = open(self.storage_file, "wb")
                        pickle.dump(self.sess.cookies, storage_file_obj)
                        storage_file_obj.close()
                        print("LOGIN SUCESS")
                        return True
            elif login_status == "1":
                print("LOGIN SUCESS")
                return True
            else:
                pass
        return False

    def logout(self, box_id):
        print("Try to logout")
        url = urljoin(BASE_URL, "auth/confirmLogout")
        payload = {"boxId": box_id}
        response = self.sess.get(url, params=payload)
        if response.status_code == 200:
            print("Logout success")
            return True

        return False

    def find_stream_url(self, page_url):
        print("#### FIND STREAM URL")
        print(page_url)
        response = self.sess.get(page_url)
        if response.status_code == 200:
            pattern = re.compile(r'streamUrl.*src:\s?"(.*)"')
            urls = re.findall(pattern, response.text)
            if len(urls) > 0:
                if "preview" in urls[0]:
                    print("Preview link found. Retry login")
                    print(urls[0])
                    self.login()
                    new_response = self.sess.get(page_url)
                    urls = re.findall(pattern, new_response.text)
                    print(urls)

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
        ]

        return [section for section in sections if section["name"] and section["url"]]

    def get_channels(self, url):
        """
        get all programme by channel from given section url
        :param url:
        :return:
        """

        print("### URL")
        print(url)

        # {
        #    "name": "KTV",
        #    "url": "https://www.yupptv.com/channels/ktv-hd/live",
        #    "image": "https://d229kpbsb5jevy.cloudfront.net/tv/150/150/bnw/ktv-HD-white.png",
        # },

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
        print("##### get programmeee")
        print(url)

        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        programmes = []
        for item in soup.find_all("a"):
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

        print(programmes)
        return programmes

    def get_episodes(self, url):
        """
        get all episodes from given url
        :param url:
        :return:
        """

        print("########## episodes")
        print("URL : {}".format(url))

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

        print("########## get stream url")
        print("URL: {}".format(url))

        stream_urls = []
        self.find_stream_url(url)
        return [{"name": "Test", "quality": "", "quality_icon": "", "url": ""}]
