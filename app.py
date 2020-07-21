import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse


def file_load(file):
    # todo: check if it's a text file
    f = open(file, 'r')
    lines = f.read().splitlines()  # Company names are listed using newlines
    f.close()
    return lines

def fetch_result(company_name):
    url = 'https://www.google.com/search?client=ubuntu&channel=fs&q={}&ie=utf-8&oe=utf-8'.\
        format(company_name)
    result = requests.get(url)
    return result


def extract_links(html):
    result_links = []
    soup = BeautifulSoup(html, 'html.parser')
    a_tags = soup.find_all('a')
    for a_tag in a_tags:
        k = a_tag.get('href')
        
        m = re.search("(?P<url>https?://[^\s]+)", k)
        n = m.group(0)
        rul = n.split('&')[0]
        domain = urlparse(rul)
        if(re.search('google.com', domain.netloc)):
            continue
        else:
            result_links.append(rul)
    return result_links


# if __name__ == '__main__':
#     print(fetch_result("http://google.com"))

