import re
import helper as helper


# To load Vidmad Video stream url
def load_vidmad_video(url):
    soup = helper.get_soup_from_url(url)
    script = soup.find_all('script', type="text/javascript")
    regex = re.compile('file:"(.*?),')
    videofile = re.findall(regex, str(script))
    return videofile[0].rstrip('"')


# To load Fastplay Video stream url
def load_fastplay_video(url):
    soup = helper.get_soup_from_url(url)
    script = soup.find_all('script', type="text/javascript")
    regex = re.compile('file:"(.*?),')
    videofile = re.findall(regex, str(script))
    return videofile[0].rstrip('"')
