import os
import argparse
import base64
import json

class Indexer(object):
    def __init__(self, stored_files_dir, storage_dir):
        self.forward_index = dict()
        self.inverted_index = dict()
        self.stored_files_dir = stored_files_dir
        self.storage_dir = storage_dir
        self.url_to_id = dict()
        self.doc_count = 0

    def create_indexes(self):
        stored_files_dir = self.stored_files_dir
        for file in os.listdir(stored_files_dir):
            opened_file = open(os.path.join(stored_files_dir, file))
            parsed_document = (opened_file.read()).split(" ")
            self.add_document(base64.b16decode(file), parsed_document)

        self.save_on_disk(self.storage_dir)
    
    def add_document(self, url, text):
        self.doc_count += 1
        self.url_to_id[url] = self.doc_count
        self.forward_index[self.doc_count] = text
        for position, word in enumerate(text):
            if word not in self.inverted_index:
                self.inverted_index[word] = []
            self.inverted_index[word].append((position,self.doc_count))
        
    def save_on_disk(self, storage_dir):
        inverted_index_file_name = os.path.join(storage_dir, "inverted_index")
        forward_index_file_name = os.path.join(storage_dir, "forward_index")
        url_to_id_file_name = os.path.join(storage_dir, "url_to_id")

        inverted_index_file = open(inverted_index_file_name, "w")
        forward_index_file = open(forward_index_file_name, "w")
        url_to_id_file = open(url_to_id_file_name, "w")

        json.dump(self.inverted_index, inverted_index_file, indent = 4)
        json.dump(self.forward_index, forward_index_file, indent = 4)
        json.dump(self.url_to_id, url_to_id_file, indent = 4)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--stored_files_dir", required = True)
    ap.add_argument("-sd", "--storage_dir", required = True)
    args = vars(ap.parse_args())
    indexer = Indexer(args["stored_files_dir"], args["storage_dir"])
    indexer.create_indexes()

if __name__ == "__main__":
    main()




