from couchdb_compose.__main__ import main


def test_show(composer):
    main(['show'], composer)


def test_push(couchdb, composer):
    assert composer.doc['_id'] not in couchdb
    main(['push', couchdb.dbname], composer)

    assert composer.doc['_id'] in couchdb

    assert (composer.doc['_id'] + ':view-deploy') not in couchdb
    main(['push', couchdb.dbname, '--deploy-views'], composer)
    assert (composer.doc['_id'] + ':view-deploy') in couchdb


def test_deploy_views(couchdb, composer):
    assert composer.doc['_id'] not in couchdb
    main(['deploy_views', couchdb.dbname], composer)
    assert (composer.doc['_id'] + ':view-deploy') in couchdb

def test_drop_viewdata(couchdb, composer):
    test_push(couchdb, composer)
    main(['drop_viewdata', couchdb.dbname], composer)
    import time
    time.sleep(1)  # wait for restart
    assert composer.doc['_id'] not in couchdb

    # ensure we worked around COUCHDB-1491
    test_deploy_views(couchdb, composer)
