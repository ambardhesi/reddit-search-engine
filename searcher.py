import os
import json
import argparse
import base64
import os
from bs4 import BeautifulSoup

class Searcher(object):
    def __init__(self, inv_index_storage_dir):
        self.inverted_index = dict()
        self.id_to_url = dict()

        inv_index_filename = os.path.join(inv_index_storage_dir, "inverted_index")
        inv_index_file = open(inv_index_filename)
        url_to_id_filename = os.path.join(inv_index_storage_dir, "url_to_id")
        url_to_id_file = open(url_to_id_filename)

        self.inverted_index = json.load(inv_index_file)
        url_to_id = json.load(url_to_id_file)

        self.id_to_url = { v : k for k, v in url_to_id.iteritems()}

    def find_docs(self, words):
        doc_list = []
        for word in words:
            doc_list.append(self.inverted_index[word])
        return doc_list

    def get_url(self, id):
        return self.id_to_url[id]

def main():
    ap = argparse.ArgumentParser() 
    ap.add_argument("-i", "--index_dir", required = True)
    args = vars(ap.parse_args())
    searcher = Searcher(args["index_dir"]) 
        
if __name__ == "__main__":
    main()





