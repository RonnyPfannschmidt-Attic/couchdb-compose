"""
couchdb-compose composes your couchdb  documents

usage: couchdb-compose show [options]
       couchdb-compose push DATABASE [--deploy-views] [options]
       couchdb-compose deploy_views DATABASE [options]
       couchdb-compose drop_viewdata DATABASE [options]

subcommands:
    show           - show the ddoc
    push           - push to the DATABASE
    deploy_views   - deploy view updates (usefull before push)
    drop_viewdata  - drop all view data and clean up the db

options: 
    -h, --help      help
    --path PATH     different path for the default composer [default: ./]
    --deploy-views  deploy views before pushing the ddoc

"""

from __future__ import print_function
import py

def _dispatch(args, composer):
    g = globals()
    for key in args:
        if key in g and args[key]:
            return g[key](args, composer)

    raise ValueError(args)


def show(args, composer):
    py.std.json.dump(composer.doc, py.std.sys.stdout, indent=1, sort_keys=True)


def push(args, composer):
    db = get_database(args)
    if args['--deploy-views']:
        deploy_views(args, composer)

    print('storing to', db, composer.doc['_id'])
    # we copy here to avoid _rev being set
    db.save_doc(composer.doc.copy(), force_update=True)


def deploy_views(args, composer):
    db = get_database(args)
    newid = composer.doc['_id'] + ":view-deploy"
    print('storing to', db, newid)
    newdoc = dict(composer.doc, _id=newid)
    view_basename = newid.split('/', 1)[1] + '/'

    db.save_doc(newdoc, force_update=True)

    for name, view in newdoc.get('views', {}).items():
        if isinstance(view, dict) and 'map' in view:
            print('request view', view_basename + name)
            db.view(view_basename + name, limit=0, stale='update_after').first()
            break  # stop after the first

    #XXX worst progres bar ever :P
    found = True
    while found:
        py.std.time.sleep(.1)
        tasks = db.server.active_tasks()
        found = False
        for task in tasks:
            if (task['database'] == db.dbname
                and task['design_document'] == newdoc['_id']):
                found = True
                print('progress', task['progress'], end='\r')
    print('done       ')


def drop_viewdata(args, composer):
    db = get_database(args)
    print('removing all ddocs')
    for ddoc in db.all_docs(startkey='_design', endkey='_desigo'):
        db.delete_doc(ddoc['id'])
    print('view cleanup')
    db.view_cleanup()
    # restart to work around COUCHDB-1491
    # - unexpected normal termination of viewserver
    db.server.res.post('/_restart', headers={"Content-Type": "application/json"})

def get_database(args):
    name_or_uri = args["DATABASE"]
    import couchdbkit
    if '/' in name_or_uri:
        return couchdbkit.Database(name_or_uri)
    else:
        return couchdbkit.Server().get_or_create_db(name_or_uri)


