from resources.scrapers import tamilyogi_scraper
from resources.lib import stream_resolver

url = stream_resolver.load_vidmad_video('http://vidmad.net/embed-9iejdznxifly.html')
print(url)