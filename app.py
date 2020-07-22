import requests
from bs4 import BeautifulSoup
import re
import os
from urllib.parse import urlparse


def is_valid_file(file_path):
    if not file_path.endswith('.txt'):
        raise TypeError("invalid file")
    elif not os.path.exists(file_path):
        raise FileNotFoundError
    else:
        return True


def get_url(company_name):
    url = 'https://www.google.com/search?client=ubuntu&channel=fs&q={}&ie=utf-8&oe=utf-8'.\
        format(company_name)
    return url


def file_load(file):
    f = open(file, 'r')
    lines = f.read().splitlines()  # Company names are listed using newlines
    f.close()
    return lines

def fetch_result(company_name):
    result = requests.get(get_url(company_name))
    return result


def extract_links(html):
    result_links = []
    soup = BeautifulSoup(html, 'html.parser')
    a_tags = soup.find_all('a')
    for a_tag in a_tags:
        k = a_tag.get('href')
        try:
            m = re.search("(?P<url>https?://[^\s]+)", k)
            n = m.group(0)
            rul = n.split('&')[0]
            domain = urlparse(rul)
            if(re.search('google.com', domain.netloc)):
                continue
            else:
                result_links.append(rul)
        except:
            continue   
    return result_links


def get_facebook_link(links):
    fb_links = list(filter(lambda a: "facebook.com" in a, links))
    if len(fb_links) > 0:
        return fb_links[0]
    return ''


def get_facebook_about_link(link):
    about_url = link+'about'
    return about_url
    