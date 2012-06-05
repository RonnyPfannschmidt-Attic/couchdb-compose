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
