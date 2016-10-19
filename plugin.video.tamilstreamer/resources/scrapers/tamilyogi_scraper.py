from ..lib import helper
import pprint

def movie_loader(url):
    """
    	Load TamilYogi main page
    	:url - tamilyogi
    	:title, image, movie page and next page url of main page.
    	"""

    movies = []
    added = []
    nextpage = ''
    img = ''
    soup = helper.get_soup_from_url(url)

    for a in soup.find_all('a'):
        title = a.get('title')
        try:
            nextpagetag = a.get('class')
            if 'next' in nextpagetag:
                nextpage = a.get('href')
        except:
            pass

        try:
            img = a.find('img')['src']
        except:
            pass

        if (title is not None) and (title != 'Tamil Movie Online') and img != '':
            try:
                if title not in added:
                    d = {'name': helper.movie_name_resolver(title),
                         'image': img,
                         'url': a.get('href')
                         }
                    movies.append(d)
                    added.append(title)
            except:
                pass

    return movies, nextpage
