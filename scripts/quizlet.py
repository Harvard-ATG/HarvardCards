#!/usr/bin/env python

# This is a simple script to fetch sample flashcard data from 
# Quizlet (http://quizlet.com/) using the developer API.
#
# It supports one basic operation: download the entire contents
# of a quizlet "set" (a set is a collection of terms) and then
# transform the data to a format suitable for import into
# the harvard cards application.
#
# Usage:
#
# python quizlet.py <client_id> <set_id> --cache
# python quizlet.py --help
#
# Notes:
#
# -The client_id comes from your developer API key on the quizlet api dashboard
# (https://quizlet.com/api_dashboard/).
#
# -The set_id comes from the quizlet set (i.e. collection of terms) that you want
# to retrieve.
#
# -The "cache" command-line option will cache the data returned by the API on
# disk so that subsequent calls will be much faster (and will avoid hitting the API
# too much). This is disabled by default, but recommended if the same set is
# going to be called repeatedly.

import argparse
import urllib2
import json

class QuizletCLI:
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
        set_transformed = QuizletSetTransformer(set_data).output()

        print set_transformed

class QuizletAPI:
    def __init__(self, client_id, cache):
        self.client_id = client_id
        self.cache = cache

    def fetch_set(self, set_id):
        cache_id = "set-{0}.json".format(set_id)
        set_data = self.load_from_cache(cache_id)
        if(set_data is False):
            self.log("fetching set {0} from quizlet api...".format(set_id))
            set_url = "https://api.quizlet.com/2.0/sets/{0}?client_id={1}".format(set_id, self.client_id)
            f = urllib2.urlopen(set_url)
            set_data = f.read()
            self.save_to_cache(cache_id, set_data)
        return set_data

    def save_to_cache(self, cache_id, cache_data):
        if(self.cache):
            try:
                with open(cache_id, 'w') as f:
                    self.log("writing cache file: {0}".format(cache_id))
                    f.write(cache_data)
            except IOError as e:
                self.log("Error saving cache file {0}: {1} {2}".format(cache_id,
                    e.errno, e.strerror))

    def load_from_cache(self, cache_id):
        if(self.cache):
            try: 
                with open(cache_id, 'r') as f:
                    self.log("loading from cache...")
                    return f.read()
            except IOError:
                return False
        return False;

    def log(self, logstr):
        print logstr

        
class QuizletSetTransformer:
    def __init__(self, set_data):
        self.set_data = set_data

    def output(self):
        return self.set_data

cli = QuizletCLI()
cli.run()
