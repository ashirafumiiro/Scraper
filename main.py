import app
import sys
import re
import requests
from bs4 import BeautifulSoup


if __name__ == "__main__":
    file_name = ''
    if len(sys.argv) == 1:
        print('please specificy a file to use')
    else:
        file_name = sys.argv[1]
    if file_name:
        try:
            if app.is_valid_file(file_name):
                companies = app.file_load(file_name)
                for company in companies:
                    email = ''
                    response  = app.fetch_result(company)
                    result_links = app.extract_links(response.text)
                    fb_links = list(filter(lambda a: "facebook.com" in a, result_links))
                    print("---------{}--------".format(company))
                    if len(fb_links) > 0:
                        print("Fb link found", fb_links[0])
                        try:
                            about_url = fb_links[0]+'about'
                            print(about_url)
                            get_about_page = requests.get(about_url)
                            soup = BeautifulSoup(get_about_page.text, 'html.parser')
                            links = soup.find_all('a')
                            email_a_tag = list(filter(lambda a: 'mailto' in a.get('href'), links))
                            if len(email_a_tag)>0:
                                href_string = str(email_a_tag[0].get('href'))
                                print("type:", str(type(href_string)),
                                      ",Value:", href_string)
                                m = re.search('mailto:(?P<email>.*)', href_string)
                                if m:
                                    mail = m.group('email')
                                    email = mail

                            else:
                                print("No email")
                        except Exception as e:
                            print(e)
                    else:
                        print("No FB link in results")
                    f = open('output.txt', 'a')
                    f.write(company+" : "+ email+'\n')
                    f.close()
                    print("\n\n")
        except FileNotFoundError as ex:
            print("File does not exist")
        except TypeError:
            print("Invalid file sent")

    
