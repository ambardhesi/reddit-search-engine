import requests
from bs4 import BeautifulSoup
import argparse
import os
import binascii
import time

class Crawler(object):
    def __init__ (self, starting_url, storage_dir):
        self.starting_url = starting_url
        self.storage_dir = storage_dir

    def download_url(self, url):
        headers = { 'User-Agent' : 'Searching Reddit bot'}
        r = requests.get(url, headers)
        if r.status_code != 200:
            raise Exception ("Error! Status code {}".format(r.status_code))
        return r.text

    def absolute_url(self, link):
        return ('https://www.reddit.com' + link)

    def TextParser(self, html):
        bs = BeautifulSoup(html)
        return bs.select('div.usertext-body')[1].text

    def crawl(self):
        currentUrl = self.starting_url
        while True:
            post_links = []
            time.sleep(1)
            print "Currently on page", currentUrl
            currentUrl_text = self.download_url(currentUrl)  
            bs = BeautifulSoup(currentUrl_text)
            all_post_links = bs.findAll('a', { "class" : "title"})
            
            try:
                for link in all_post_links:
                    if link["href"].startswith("/r/Gunners"):
                        post_links.append(self.absolute_url(link["href"])) 

                for link in post_links:
                    print "ON PAGE : ", link
                    parsedText = self.TextParser(self.download_url(link)) 
                    file_name = os.path.join(self.storage_dir, binascii.hexlify(link))
                    opened_file = open(file_name, "w")
                    opened_file.write(parsedText.encode('utf8'))
                    time.sleep(2)
            except Exception:
                print "An error occured :("

            next_page_url = bs.find('a', {"rel" : "next"})["href"]
            currentUrl = next_page_url
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
