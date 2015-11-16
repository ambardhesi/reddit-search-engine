import requests
from bs4 import BeautifulSoup
import time
import os
import base64 
import argparse

def downloadRedditUrl(url): 
    headers = {
            'User-Agent' : 'SearchingReddit bot version 0.1' 
            }
    r = requests.get(url, headers = headers)
    if r.status_code != 200:
        raise Exception("Not okay! Status code : {}".format(r.status_code))
    return r.text

def parseData(html):
    bs = BeautifulSoup(html)
    return bs.select('div.usertext-body')[1].text


class Crawler(object):
    def __init__(self, start_url, storage_dir):
        self.start_url = start_url
        self.storage_dir = storage_dir
    
    def make_absolute_url(self, url):
        return ("https://reddit.com" + url)

    def crawl(self):
        current_page_url = self.start_url
        while True:
            post_links = []
            crawled_urls = 0
            print "Current page is {}".format(current_page_url)
            current_page = downloadRedditUrl(current_page_url)
            bs = BeautifulSoup(current_page)
            all_post_links = bs.findAll("a", attrs = {'class' : 'title'})
            try:
                for link in all_post_links:
                    if link["href"].startswith('/r/Gunners'):
                        post_links.append(self.make_absolute_url(link["href"]))
            #post_links = [self.make_absolute_url(link["href"]) for link in all_post_links]
                for link in post_links:
                    print "Crawling link {}".format(link)
                    text = parseData(downloadRedditUrl(link))  
                    stored_text_file_name = os.path.join(self.storage_dir, base64.b16encode(link))
                    stored_text_file = open(stored_text_file_name, "w")
                    stored_text_file.write(text.encode('utf8'))
                    crawled_urls += 1
                    time.sleep(2)
            except Exception:
                print "An error occured!"                    

            next_page_url = bs.find('a', attrs = {'rel' : 'next'})['href']           
            current_page_url = next_page_url
            print "Total crawled URLS from this page {}".format(crawled_urls)
            time.sleep(2)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--start_url", required = True,
            help = "URL of starting link")
    ap.add_argument("-d", "--storage_dir", required = True,
            help = "Path to where files will be stored.")
    args = vars(ap.parse_args())
    
    crawler = Crawler(args["start_url"], args["storage_dir"])
    crawler.crawl()

if __name__ == "__main__":
    main()
