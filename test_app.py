import unittest
import re
import os
from app import (file_load, fetch_result, extract_links, is_valid_file, get_url,
    get_facebook_about_link, get_facebook_link)


class TestBuildURL(unittest.TestCase):
    def test_get_url(self):
        company_name = "Innovex"
        regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        self.assertIsNotNone(re.match(regex, get_url(company_name)))



class TestIsValidFile(unittest.TestCase):
    def test_is_valid_file(self):
        valid_file = 'test.txt'
        invalid_file = 'test.sh'
        f = open(valid_file, 'w')
        f.write('test')
        f.close()
        self.assertTrue(is_valid_file(valid_file))
        with self.assertRaises(TypeError):
            is_valid_file(invalid_file)
        os.remove(valid_file)
        with self.assertRaises(FileNotFoundError):
            is_valid_file(valid_file)




class TestFileLoad(unittest.TestCase):
    def test_loading_file(self):
        companies = ['Concept Sauce', 'Google', 'Microsoft', 'Amazon']
        file_name = 'test_file.txt'
        f = open(file_name, 'w')
        for line in companies:
            f.write(line+'\n')
        f.close()
        result = file_load(file_name)
        os.remove(file_name)
        self.assertEqual(result, companies)


class TestResponse(unittest.TestCase):
    def test_response(self):
        result = fetch_result('Concept Sauce')
        self.assertEqual(result.status_code, 200)
    

class TestExtractLinks(unittest.TestCase):
    def test_extract_links(self):
        html_doc = """
            <html><head><title>The Dormouse's story</title></head>
            <body>
            <p class="title"><b>The Dormouse's story</b></p>

            <p class="story">Once upon a time there were three little sisters; and their names were
            <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
            <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
            <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
            and they lived at the bottom of a well.</p>
            <a href="https://google.com/some/google/resource">Ignored</a>
            <p class="story">...</p>
        """
        links = extract_links(html_doc)
        self.assertEqual(links[0], 'http://example.com/elsie')
        self.assertEqual(links[2], 'http://example.com/tillie')
        self.assertEqual(len(links), 3)  # must ignore links from google resources


class TestFacebookLinks(unittest.TestCase):
    def test_fb_link(self):
        self.assertGreater(len(get_facebook_link(['http://facebook.com/mycompany/'])),0)
        self.assertEqual(len(get_facebook_link(['http://no.com/valid/link'])), 0)
    
    def test_fb_about(self):
        fb_link = 'http://facebook.com/mycompany'
        about_link = get_facebook_about_link(fb_link)
        self.assertTrue('about' in about_link)

