from resources.scrapers import tamilyogi_scraper
import pprint

url = 'http://tamilyogi.cc/category/tamilyogi-full-movie-online/'
movies, nextpage = tamilyogi_scraper.movie_loader(url)

pprint.pprint(movies)
