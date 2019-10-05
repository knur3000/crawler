from bs4 import BeautifulSoup
import urllib3
import morfeusz2
import yaml
import datetime


def count_nouns(titles: list):
    """Return dictionary of occurences of nouns(nominative) in article titles"""
    morf = morfeusz2.Morfeusz()
    unique_list: list = []

    for title in titles:
        sentence_analysis: list = morf.analyse(title)

        for id in range(len(sentence_analysis)):
            list_matching_words = [item for item in sentence_analysis if item[0] == id]
            unique_list.append(list_matching_words)

    words_to_check: list = []
    for unique_word in unique_list:

        for item in unique_word:
            compatible_types: bool = any(elem in item[-1][3]
                                         for elem in ['nazwisko', 'imiona', 'imię', 'nazwa_geograficzna'])

            if (('subst:sg:nom:f' in item[-1][2] or 'subst:sg:nom:m' in item[-1][2]
                 or 'subst:pl:nom:f' in item[-1][2] or 'subst:pl:nom:m' in item[-1][2])
                    and not (compatible_types or ':' in item[-1][1])):

                words_to_check.append(item[-1][1])
            else:
                pass

    results: dict = {}
    for word in words_to_check:
        results.setdefault(word, 0)
        results[word] += 1

    return results


def extract_tiles(url):
    """Uses BS4 to extract titles from RSS feeds"""
    http = urllib3.PoolManager()
    response = http.request('GET', url)

    soup = BeautifulSoup(response.data, "xml")
    soup_titles = soup.find_all("title")
    titles: list = [title.text for title in soup_titles]

    return titles


def run():
    """ Runs the crawler"""

    distinct: dict = {}

    with open('urls.yaml') as f:
        urls = yaml.load(f, Loader=yaml.FullLoader)
        for sites in urls:
            slownik = count_nouns(extract_tiles(sites))
            for key, count in slownik.items():
                distinct.setdefault(key,0)
                distinct[key] += count


    return {"Date": str(datetime.date.today()), "Results": distinct}


print(run())
