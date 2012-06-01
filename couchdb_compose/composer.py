import py
import yaml
import copy

class Composer(object):
    def __init__(self, path):

        self.path = path
        with path.join('couchdb-compose.yml').open() as fp:
            self.config = yaml.load(fp)
        self.doc = copy.deepcopy(self.config['doc'])

    def push(self, attrs, data):
        d = self.doc
        for attr in attrs[:-1]:
            d = d.setdefault(attr, {})
        d[attrs[-1]] = data #XXX: conflicts

from .ddoc import load_objects
from .preprocess import run_preprocessors

actions = [load_objects, run_preprocessors]


