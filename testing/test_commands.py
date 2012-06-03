from couchdb_compose.__main__ import show, push, parser
from couchdb_compose.composer import Composer
import argparse

from .test_acceptance import examplesdir


def test_show():
    composer = Composer(examplesdir/'streamsapp')
    show({}, composer)



def test_push(couchdb):
    composer = Composer(examplesdir/'streamsapp')
    assert composer.doc['_id'] not in couchdb
    push(argparse.Namespace(database=couchdb.dbname), composer)
    
    assert composer.doc['_id'] in couchdb
