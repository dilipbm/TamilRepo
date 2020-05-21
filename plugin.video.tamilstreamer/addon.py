import pprint
from datetime import datetime, timedelta
import ast
import time as timee
import re
import os

import routing
import xbmcgui
import xbmcvfs
from xbmcgui import ListItem
from xbmcplugin import addDirectoryItem, endOfDirectory, setResolvedUrl, setContent

try:
    import cPickle as pickle
except ImportError:
    import pickle

from resources.lib import tamilyogi
from resources.lib import tamilrasigan
from resources.lib import tamilgun
from resources.lib import tamildbox
from resources.lib import thiraimix
from resources.lib import tamilarasan
from resources.lib import tamildhool
from resources.lib import yupptv
from resources.lib import tamilan
from resources.lib import utils

plugin = routing.Plugin()

directory = os.path.dirname(os.path.realpath(__file__))
storage_file = os.path.join(directory, "storage")
ytv = yupptv.Yupptv(plugin, storage_file)
tamilan = tamilan.Tamilan()

# SITE VIEW - MAIN VIEW
@plugin.route("/")
def index():
    """
    All site here
    :return:
    """

    addDirectoryItem(
        plugin.handle,
        plugin.url_for(section_view, site_name="tamilyogi"),
        ListItem("Tamil Yogi"),
        True,
    )
    addDirectoryItem(
        plugin.handle,
        plugin.url_for(section_view, site_name="tamilgun"),
        ListItem("Tamilgun"),
        True,
    )
    addDirectoryItem(
        plugin.handle,
        plugin.url_for(section_view, site_name="tamildbox"),
        ListItem("Tamildbox"),
        True,
    )
    # addDirectoryItem(plugin.handle, plugin.url_for(section_view, site_name="thiraimix"), ListItem("ThiraiMix"), True)
    addDirectoryItem(
        plugin.handle,
        plugin.url_for(section_view, site_name="tamilarasan"),
        ListItem("Tamilarasan"),
        True,
    )
    addDirectoryItem(
        plugin.handle,
        plugin.url_for(section_view, site_name="tamildhool"),
        ListItem("TamilDhool"),
        True,
    )
    addDirectoryItem(
        plugin.handle,
        plugin.url_for(section_view, site_name="yupptv"),
        ListItem("YuppTV"),
        True,
    ),
    addDirectoryItem(
        plugin.handle,
        plugin.url_for(section_view, site_name="tamilan"),
        ListItem("Tamilan.NET"),
        True,
    )

    # addDirectoryItem(plugin.handle, plugin.url_for(directplay), ListItem("Test"), True)

    endOfDirectory(plugin.handle)


# SECTION VIEW
@plugin.route("/sections/<site_name>")
def section_view(site_name):
    """
    all sections by sites. sections are getted from site api
    :param site_name:
    :return:
    """

    setContent(plugin.handle, "files")

    if site_name == "tamilyogi":
        site_api = tamilyogi.TamilYogi(plugin)

        for section in site_api.get_sections():
            addDirectoryItem(
                plugin.handle,
                plugin.url_for(
                    movies_view,
                    site_name=site_name,
                    section_url=utils.encode_url(section["url"]),
                ),
                ListItem(section["name"]),
                True,
            )

    elif site_name == "tamilrasigan":
        site_api = tamilrasigan.TamilRasigan(plugin)

        for section in site_api.get_sections():
            addDirectoryItem(
                plugin.handle,
                plugin.url_for(
                    movies_view,
                    site_name=site_name,
                    section_url=utils.encode_url(section["url"]),
                ),
                ListItem(section["name"]),
                True,
            )

    elif site_name == "thiraimix":
        site_api = thiraimix.Thiraimix(plugin)
        for section in site_api.get_sections():
            addDirectoryItem(
                plugin.handle,
                plugin.url_for(
                    movies_view,
                    site_name=site_name,
                    section_url=utils.encode_url(section["url"]),
                ),
                ListItem(section["name"]),
                True,
            )

    elif site_name == "tamilgun":
        site_api = tamilgun.Tamilgun(plugin)
        for section in site_api.get_sections():
            addDirectoryItem(
                plugin.handle,
                plugin.url_for(
                    movies_view,
                    site_name=site_name,
                    section_url=utils.encode_url(section["url"]),
                ),
                ListItem(section["name"]),
                True,
            )

    elif site_name == "tamildbox":
        site_api = tamildbox.Tamildbox(plugin)
        for section in site_api.get_sections():
            addDirectoryItem(
                plugin.handle,
                plugin.url_for(
                    movies_view,
                    site_name=site_name,
                    section_url=utils.encode_url(section["url"]),
                ),
                ListItem(section["name"]),
                True,
            )

    elif site_name == "tamilarasan":
        site_api = tamilarasan.Tamilarasan(plugin)
        for section in site_api.get_sections():
            addDirectoryItem(
                plugin.handle,
                plugin.url_for(
                    movies_view,
                    site_name=site_name,
                    section_url=utils.encode_url(section["url"]),
                ),
                ListItem(section["name"]),
                True,
            )

    elif site_name == "tamildhool":
        site_api = tamildhool.TamilDhool(plugin)
        for section in site_api.get_sections():
            addDirectoryItem(
                plugin.handle,
                plugin.url_for(
                    programmes_view,
                    site_name=site_name,
                    url=utils.encode_url(section["url"]),
                ),
                ListItem(section["name"]),
                True,
            )

    elif site_name == "yupptv":
        for section in ytv.get_sections():
            addDirectoryItem(
                plugin.handle,
                plugin.url_for(
                    channel_view,
                    site_name=site_name,
                    url=utils.encode_url(section["url"]),
                ),
                ListItem(section["name"]),
                True,
            )

    elif site_name == "tamilan":
        for section in tamilan.get_sections():
            addDirectoryItem(
                plugin.handle,
                plugin.url_for(
                    movies_view,
                    site_name=site_name,
                    section_url=utils.encode_url(section["url"]),
                ),
                ListItem(section["name"]),
                True,
            )
    # elif site_name == "yupptvlive":
    #    url = ytv.find_stream_url("https://www.yupptv.com/channels/sun-tv-hd/live")
    #    plugin.redirect("/playable/{}/{}".format("playable", utils.encode_url(url)))

    endOfDirectory(plugin.handle)


@plugin.route("/channel/<site_name>/<url>")
def channel_view(site_name, url):
    url = utils.decode_url(url)

    if site_name == "yupptv":
        channels = ytv.get_channels(url)
        for channel in channels:
            listitem = ListItem(channel["name"])
            listitem.setThumbnailImage(channel["image"])
            if url == "live":
                addDirectoryItem(
                    plugin.handle,
                    plugin.url_for(
                        episode_view,
                        site_name=site_name,
                        url=utils.encode_url(channel["url"]),
                    ),
                    listitem,
                    True,
                )
                # plugin.redirect(
                #    "/playable/{}/{}".format(channel["name"], utils.encode_url(url))
                # )

            elif url == "catchup":
                addDirectoryItem(
                    plugin.handle,
                    plugin.url_for(
                        day_view,
                        site_name=site_name,
                        url=utils.encode_url(channel["url"]),
                    ),
                    listitem,
                    True,
                )

    endOfDirectory(plugin.handle)


@plugin.route("/day/<site_name>/<url>")
def day_view(site_name, url):
    url = utils.decode_url(url)

    if site_name == "yupptv":
        for idx in range(10):
            listitem = ListItem(
                (datetime.now() - timedelta(days=idx)).strftime("%a - %d %b")
            )
            addDirectoryItem(
                plugin.handle,
                plugin.url_for(
                    programmes_view,
                    site_name=site_name,
                    url=utils.encode_url("{}/{}".format(url, idx + 1)),
                ),
                listitem,
                True,
            )

    endOfDirectory(plugin.handle)


@plugin.route("/programmes/<site_name>/<url>")
def programmes_view(site_name, url):

    url = utils.decode_url(url)

    if site_name == "thiraimix":
        site_api = thiraimix.Thiraimix(plugin)
        programmes = site_api.get_programmes(url)

        for programme in programmes:
            listitem = ListItem(programme["name"])
            listitem.setThumbnailImage(programme["image"])
            addDirectoryItem(
                plugin.handle,
                plugin.url_for(
                    episode_view,
                    site_name=site_name,
                    url=utils.encode_url(programme["url"]),
                ),
                listitem,
                True,
            )

    elif site_name == "tamildhool":
        site_api = tamildhool.TamilDhool(plugin)
        programmes = site_api.get_programmes(url)

        for programme in programmes:
            listitem = ListItem(programme["name"])
            listitem.setThumbnailImage(programme["image"])
            addDirectoryItem(
                plugin.handle,
                plugin.url_for(
                    episode_view,
                    site_name=site_name,
                    url=utils.encode_url(programme["url"]),
                ),
                listitem,
                True,
            )

    elif site_name == "yupptv":
        programmes = ytv.get_programmes(url)
        for programme in programmes:
            listitem = ListItem(programme["name"])
            listitem.setThumbnailImage(programme["image"])
            addDirectoryItem(
                plugin.handle,
                plugin.url_for(
                    episode_view,
                    site_name=site_name,
                    url=utils.encode_url(programme["url"]),
                ),
                listitem,
                True,
            )

    endOfDirectory(plugin.handle)


@plugin.route("/episodes/<site_name>/<url>")
def episode_view(site_name, url):

    url = utils.decode_url(url)

    if site_name == "thiraimix":
        site_api = thiraimix.Thiraimix(plugin)
        episodes = site_api.get_episodes(url)

    elif site_name == "tamildhool":
        site_api = tamildhool.TamilDhool(plugin)
        episodes = site_api.get_episodes(url)

    elif site_name == "yupptv":
        if "live" in url:
            url = ytv.find_stream_url(url)
            plugin.redirect(
                "/playable/{}/{}".format("Play Live", utils.encode_url(url))
            )

        else:
            url = ytv.find_stream_url(url)
            plugin.redirect("/playable/{}/{}".format("Play", utils.encode_url(url)))

        return

    for episode in episodes:
        addDirectoryItem(
            plugin.handle,
            plugin.url_for(
                stream_list_view,
                site_name=site_name,
                movie_name=episode["prog_name"],
                movie_url=utils.encode_url(episode["url"]),
            ),
            ListItem(episode["name"]),
            True,
        )

    endOfDirectory(plugin.handle)


@plugin.route("/movies/<site_name>/<section_url>")
def movies_view(site_name, section_url):
    """
    show all movies from url (section_url).
    :param site_name:
    :param section_url:
    :return:
    """

    setContent(plugin.handle, "movies")

    section_url = utils.decode_url(section_url)

    if site_name == "tamilyogi":
        site_api = tamilyogi.TamilYogi(plugin)

    elif site_name == "tamilrasigan":
        site_api = tamilrasigan.TamilRasigan(plugin)

    elif site_name == "tamilgun":
        site_api = tamilgun.Tamilgun(plugin)

    elif site_name == "tamildbox":
        site_api = tamildbox.Tamildbox(plugin)

    elif site_name == "tamilarasan":
        site_api = tamilarasan.Tamilarasan(plugin)

    elif site_name == "tamildhool":
        site_api = tamildhool.TamilDhool(plugin)

    elif site_name == "tamilan":
        site_api = tamilan

    movies = site_api.get_movies(section_url)

    if len(movies) == 0:
        xbmcgui.Dialog().notification("Error 404", "No movies found")
        setContent(plugin.handle, "files")
        plugin.redirect("/sections/{}".format(site_name))

    for movie in movies:
        listitem = ListItem(utils.color_movie_name(movie["name"]))
        listitem.setThumbnailImage(movie["image"])
        listitem.setArt({"thumb": movie["image"], "poster": movie["image"]})
        listitem.setInfo("video", movie["infos"])
        addDirectoryItem(
            plugin.handle,
            plugin.url_for(
                stream_list_view,
                site_name=site_name,
                movie_name=movie["name"],
                movie_url=utils.encode_url(movie["url"]),
            ),
            listitem,
            True,
        )

    endOfDirectory(plugin.handle)


@plugin.route("/playable/<name>/<url>")
def playable(name, url):
    listitem = ListItem(name)
    listitem.setProperty("IsPlayable", "true")
    addDirectoryItem(
        plugin.handle, utils.decode_url(url), listitem, False,
    )
    endOfDirectory(plugin.handle)


@plugin.route("/directplay")
def directplay():
    listitem = ListItem("test")
    listitem.setProperty("IsPlayable", "true")
    # url = ytv.find_stream_url("https://www.yupptv.com/channels/sun-tv-hd/live")

    # addDirectoryItem(
    #    plugin.handle,
    #    'https://www1411.hlsmp4.com/token=RYov85oqYWpHg890KDQYiQ/1559514826/0.0.0.0/47/6/bb/cb0147d55dfd8f9e3b9b793083480bb6-720p.mp4',
    #    listitem,
    #    False
    # )

    # url = "{}|User-Agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'".format(
    #     url
    # )

    addDirectoryItem(
        plugin.handle, url, listitem, False,
    )
    endOfDirectory(plugin.handle)

    # url = "https://yuppmsluk.akamaized.net/hls/live/2007561/jayatv/jayatv/jayatv_200/chunklist.m3u8?hdntl=exp=1590055482~acl=!*/jayatv/jayatv/*!/payload/yuppTVCom_5_5580371_79a18526b9174175_FR_82.65.54.29/*~data=hdntl~hmac=e73ae3b1d9497c206e2ceefe26eaee2dfd2bb83026d4f97de0d6a6e08e1d35e5"
    # item = {
    #     "label": "Playable",
    #     "path": url,
    #     "is_playable": True,
    # }
    # return plugin.set_resolved_url(item)


# STREAM LIST VIEW
@plugin.route("/stream_list/<site_name>/<movie_name>/<movie_url>")
def stream_list_view(site_name, movie_name, movie_url):
    """
    show all stream for the movie with quality
    :param site_name:
    :param movie_name:
    :param movie_url:
    :return:
    """

    movie_url = utils.decode_url(movie_url)

    # If hit Next page
    if movie_name == "Next Page":
        plugin.redirect("/movies/{}/{}".format(site_name, utils.encode_url(movie_url)))

    else:
        if site_name == "tamilyogi":
            site_api = tamilyogi.TamilYogi(plugin)

        elif site_name == "tamilrasigan":
            site_api = tamilrasigan.TamilRasigan(plugin)

        elif site_name == "tamilgun":
            site_api = tamilgun.Tamilgun(plugin)

        elif site_name == "thiraimix":
            site_api = thiraimix.Thiraimix(plugin)

        elif site_name == "tamildbox":
            site_api = tamildbox.Tamildbox(plugin)

        elif site_name == "tamilarasan":
            site_api = tamilarasan.Tamilarasan(plugin)

        elif site_name == "tamildhool":
            site_api = tamildhool.TamilDhool(plugin)

        elif site_name == "yupptv":
            site_api = ytv

        elif site_name == "tamilan":
            site_api = tamilan

        stream_urls = site_api.get_stream_urls(movie_name, movie_url)

        if len(stream_urls) == 0:
            xbmcgui.Dialog().notification(
                heading="Error 404", message="Video is no longer available"
            )

        else:
            for stream_url in stream_urls:
                listitem = ListItem(stream_url["name"] + " | " + stream_url["quality"])
                listitem.setInfo(type="video", infoLabels={"Title": stream_url["name"]})
                listitem.setIconImage(stream_url["quality_icon"])
                listitem.setProperty("IsPlayable", "true")
                addDirectoryItem(plugin.handle, stream_url["url"], listitem, False)

            endOfDirectory(plugin.handle)


if __name__ == "__main__":
    plugin.run()
