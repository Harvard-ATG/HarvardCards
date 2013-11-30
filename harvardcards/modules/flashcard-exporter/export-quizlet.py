#!/usr/bin/env python

# This script fetches sample flashcard data from Quizlet (http://quizlet.com/)
# using the developer API (http://quizlet.com/api).
#
# It supports one basic operation: fetch the entire contents of a quizlet "set"
# (a set is a collection of terms) and then transform the data to a format
# suitable for import into the harvard cards application.
#
# The results of the export and transformation are printed to STDOUT.  To save
# the data to a file, simply redirect the output to a file.
#
# Usage:
#
#   ./export-quizlet.py [client_id] [set_id] --cache
#   ./export-equizlet.py [client_id] [set_id] --cache > data/foo.json
#   ./export-quizlet.py --help
#
# Notes:
#
# -The client_id comes from your developer API key on the quizlet api dashboard
# (https://quizlet.com/api_dashboard/).
#
# -The set_id comes from the quizlet set (i.e. collection of terms) that you want
# to retrieve.
#
# -The "cache" command-line option is a flag (when enabled, true, otherwise
# false) that will cause the script to try and cache the data returned by the
# API. This is useful if the same set will be retrieved multiple times, since it
# will speed up the fetch and cut down on the number of hits on the quizlet API
# (we don't want to wear out our welcome). 

import argparse
import urllib2
import json
import os.path
import sys

class QuizletCLI:
    ''' 
    Handles command line interaction with the quizlet api. 
    Call the run() method to execute. Example usage:

    cli = QuizletCli()
    cli.run()

    See the -h option to see what options are expected/available.
    '''
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("client_id", help="the quizlet api client_id is required to issue requests")
        self.parser.add_argument("set_id", help="the quizlet set_id to fetch")
        self.parser.add_argument("--cache", help="read/write quizlet data from the file cache", action="store_true")

    def run(self):
        args = self.parser.parse_args()
        client_id = args.client_id
        set_id = args.set_id
        cache = args.cache

        quizlet_api = QuizletAPI(client_id, cache)
        set_data = quizlet_api.fetch_set(set_id)
        set_transformed = QuizletSetTransformer(set_data).transform()

        print json.dumps(set_transformed, sort_keys=True, indent=4, separators=(',', ': '))

class QuizletAPI:
    ''' 
    Simple wrapper class around the quizlet api.
    '''
    cache_dir = 'cache'
    def __init__(self, client_id, cache):
        self.client_id = client_id
        self.cache = cache

    def fetch_set(self, set_id):
        cache_id = self.cache_id_of_set(set_id)
        set_data = self.load_from_cache(cache_id)
        if(set_data is False):
            self.log("fetching set {0} from quizlet api...".format(set_id))
            set_url = "https://api.quizlet.com/2.0/sets/{0}?client_id={1}".format(set_id, self.client_id)
            f = urllib2.urlopen(set_url)
            set_data = f.read()

            # pretty-print the JSON to the cache so a human can examine it more
            # easily. this was added for development purposes.
            set_data_pretty = json.dumps(json.loads(set_data), sort_keys=True, indent=4, separators=(',', ': '))

            self.save_to_cache(cache_id, set_data_pretty)
        return set_data

    def save_to_cache(self, cache_id, cache_data):
        if(self.cache):
            try:
                with open(self.cache_file_path(cache_id), 'w') as f:
                    self.log("writing cache file: {0}".format(cache_id))
                    f.write(cache_data)
            except IOError as e:
                self.log("Error saving cache file {0}: {1} {2}".format(cache_id,
                    e.errno, e.strerror))

    def load_from_cache(self, cache_id):
        if(self.cache):
            try: 
                with open(self.cache_file_path(cache_id), 'r') as f:
                    self.log("loading from cache...")
                    return f.read()
            except IOError:
                return False
        return False

    def cache_file_path(self, cache_id):
        return os.path.join(QuizletAPI.cache_dir, cache_id)

    def cache_id_of_set(self, set_id):
        return "quizlet-set-{0}.json".format(set_id)

    def log(self, logstr):
        sys.stderr.write(logstr)

        
class QuizletSetTransformer:
    ''' 
    Class to transform a quizlet "set" or collection of terms into a format
    that may be consumed by harvard cards.
    '''
    def __init__(self, set_data):
        self.set_data = json.loads(set_data)
        self.output_data = {
            "collections": [{
                "collection_name": "",
                "decks": [],
            }],
            "cards_count": 0,
            "cards": []
        }
        self.collection_data = self.output_data['collections'][0]

    def update_collection(self):
        self.collection_data['collection_name'] = "Quizlet Set {0}".format(self.set_data["id"]) 

    def update_decks(self):
        terms = self.set_data["terms"]
        deck_title = self.set_data["title"]
        deck_cards = [term["id"] for term in terms]

        self.collection_data['decks'] = [{
            "deck_name": deck_title,
            "deck_cards": deck_cards
        }]

    def update_cards(self):
        terms = self.set_data["terms"]
        cards = []

        for term in terms:
            fields = [
                self.create_text_field(label="Term", value=term['term'], display=True),
                self.create_text_field(label="Definition", value=term['definition'], display=False)]
            
            if(term['image']):
                fields.append(self.create_image_field(label="Image", value=term['image'], display=False))

            cards.append({
                "_card_id": term["id"],
                "fields": fields
            })

        self.output_data['cards_count'] = len(cards)
        self.output_data['cards'] = cards

    def create_text_field(self, *args, **kwargs):
        return {
                "value": kwargs["value"],
                "type": "T",
                "label": kwargs["label"],
                "show_label": True,
                "display": kwargs["display"]
                }

    def create_image_field(self, *args, **kwargs):
        return {
                "value": kwargs["value"]["url"],
                "type": "I",
                "label": kwargs["label"],
                "show_label": False,
                "display": kwargs["display"]
                }

    def transform(self):
        self.update_collection()
        self.update_decks()
        self.update_cards()
        return self.output_data

QuizletCLI().run()
