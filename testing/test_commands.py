from couchdb_compose.__main__ import main
from couchdb_compose.composer import Composer
import argparse

from .test_acceptance import examplesdir


def test_show():
    composer = Composer(examplesdir/'streamsapp')
    main(['show'], composer)



def test_push(couchdb):
    composer = Composer(examplesdir/'streamsapp')
    assert composer.doc['_id'] not in couchdb
    main(['push', couchdb.dbname], composer)
    
    assert composer.doc['_id'] in couchdb

    assert (composer.doc['_id'] + ':view-deploy') not in couchdb
    main(['push', couchdb.dbname, '--deploy-views'], composer)
    assert (composer.doc['_id'] + ':view-deploy') in couchdb


def test_deploy_views(couchdb):
    composer = Composer(examplesdir/'streamsapp')
    assert composer.doc['_id'] not in couchdb
    main(['deploy_views', couchdb.dbname], composer)
    assert (composer.doc['_id'] + ':view-deploy') in couchdb
