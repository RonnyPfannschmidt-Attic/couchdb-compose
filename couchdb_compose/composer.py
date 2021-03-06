from __future__ import print_function
import copy
import mimetypes

class Composer(object):

    def __init__(self, path, config):
        self.path = path
        self.config = config
        self.doc = copy.deepcopy(config.get('doc', {}))

    def getlist(self, name):
        return self.config.get(name, [])

    def push(self, attrs, data):
        d = self.doc
        for attr in attrs[:-1]:
            d = d.setdefault(attr, {})
        d[attrs[-1]] = data  #XXX: conflicts

    def add_attachment_from_file(self, attachment_path):
        content = attachment_path.read()
        name = self.path.bestrelpath(attachment_path)
        self.add_attachment(name, content)

    def add_attachment(self, name, content):
        attachments = self.doc.setdefault('_attachments', {})
        info = attachments[name] = {
            'data': content,
            'content_type': mimetypes.guess_type(name)[0],
        }
        return info




    def run_actions(self, actions):
        for action in actions:
            print('* start', action.__name__)
            action(self)

from .ddoc import load_objects
from .preprocess import run_preprocessors
from .attachments import add_attachments
from .externals import include_externals
actions = [
    load_objects,
    add_attachments,
    include_externals,
    run_preprocessors,
]


