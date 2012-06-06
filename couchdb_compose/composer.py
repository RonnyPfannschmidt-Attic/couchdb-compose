from __future__ import print_function
import copy
import mimetypes

class Composer(object):

    def __init__(self, path, config):
        self.path = path
        self.config = config
        self.doc = copy.deepcopy(config.get('doc', {}))

    def push(self, attrs, data):
        d = self.doc
        for attr in attrs[:-1]:
            d = d.setdefault(attr, {})
        d[attrs[-1]] = data  #XXX: conflicts

    def add_attachment(self, attachment_path):
        attachments = self.doc.setdefault('_attachments', {})
        content = attachment_path.read()
        name = self.path.bestrelpath(attachment_path)

        attachments[name] = {'data': content, 'content_type': mimetypes.guess_type(name)[0]}



    def run_actions(self, actions):
        for action in actions:
            print('* start', action.__name__)
            action(self)

from .ddoc import load_objects
from .preprocess import run_preprocessors
from .attachments import add_attachments
actions = [load_objects, add_attachments, run_preprocessors]


