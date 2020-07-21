import requests
from bs4 import BeautifulSoup
import re


url_regex = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https:// # domain...
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

resut = requests.get("https://www.google.com")
print("Status code:", resut.status_code)
soup = BeautifulSoup(resut.content, 'html.parser')
links = soup.find_all('a')
# print(links)

for link in links:
    if "About" in link.text:
        print(link)
        print(link.attrs['href'])
