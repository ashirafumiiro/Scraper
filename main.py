import app
import sys
import re
import requests
from bs4 import BeautifulSoup


def get_file_name():
    file_name = ''
    if len(sys.argv) == 1:
        print('please specificy a file to use')
        return
    else:
        file_name = sys.argv[1]
    try:
        if app.is_valid_file(file_name):
            return file_name
    except FileNotFoundError:
        print ("File not found")
    except TypeError:
        print("Invalid file specified")
    return ''


def get_email(fb_about_link):
    get_about_page = requests.get(fb_about_link)
    soup = BeautifulSoup(get_about_page.text, 'html.parser')
    links = soup.find_all('a')
    email_a_tag = list(filter(lambda a: 'mailto' in a.get('href'), links))
    if len(email_a_tag)>0:
        href_string = str(email_a_tag[0].get('href'))
        print("Value:", href_string)
        m = re.search('mailto:(?P<email>.*)', href_string)
        if m:
            email = m.group('email')
            return email
    else:
        print("No email")
        return ''


def print_to_file(company_name, email):
    f = open('output.txt', 'a')
    f.write(company_name+" : "+ email+'\n')
    f.close()


def main():
    file_name = get_file_name()
    if not file_name:
        return
    companies = app.file_load(file_name)
    for company in companies:
        print("---------{}--------".format(company))
        response  = app.fetch_result(company)
        result_links = app.extract_links(response.text)
        fb_link = app.get_facebook_link(result_links)
        if fb_link:
            about_link = app.get_facebook_about_link(fb_link)
            email = get_email(about_link)
            print_to_file(company, email)
        print("\n\n")

    
if __name__ == "__main__":
    main()
