
from __future__ import print_function
import py


def show(args, composer):
    py.std.pprint.pprint(composer.doc, py.std.sys.stdout)


def push(args, composer):
    db = args.database
    if args.deploy_views:
        deploy_views(args, composer)

    import couchdbkit
    print('storing to', db, composer.doc['_id'])
    # we copy here to avoid _rev being set
    db.save_doc(composer.doc.copy(), force_update=True)


def deploy_views(args, composer):
    db = args.database
    newid = composer.doc['_id'] + ":view-deploy"
    print('storing to', db, newid)
    newdoc = dict(composer.doc, _id=newid)
    view_basename = newid.split('/', 1)[1] + '/'
    print(view_basename)

    db.save_doc(newdoc, force_update=True)

    for name, view in newdoc.get('views', {}).items():
        if isinstance(view, dict) and 'map' in view:
            print('request view', view_basename+name)
            db.view(view_basename+name, limit=0, stale='update_after').first()
            break # stop after the first

    found = True
    while found:
        py.std.time.sleep(.1)
        tasks = db.server.active_tasks()
        found = False
        for task in tasks:
            if task['database'] == db.dbname and \
               task['design_document'] == newdoc['_id']:
                found = True
                print('progress', task['progress'],end='\r')
    print('\ndone')


def drop_viewdata(args, composer):
    db = args.database
    print('removing all ddocs')
    for ddoc in db.all_docs(startkey='_design', endkey='_desigo'):
        db.delete_doc(ddoc['id'])
    print('view cleanup')
    db.view_cleanup()

from argparse import ArgumentParser
parser = ArgumentParser(prog='couchdb-compose')

parser.add_argument('--path', nargs='?',  default=py.path.local(), type=py.path.local)
subparsers = parser.add_subparsers()

show_parser = subparsers.add_parser('show', help='show the constructed ddoc')
show_parser.set_defaults(func=show)

push_parser = subparsers.add_parser('push', help='stores the composed doc to the db')
push_parser.set_defaults(func=push)
push_parser.add_argument('--deploy-views', action='store_true',
                         help='deploy views before pushing')


deploy_views_parser = subparsers.add_parser('deploy_views',
                                            help='stores the ddoc to a different id and updates all views, '
                                                 'usefull for view updates before a push')
deploy_views_parser.set_defaults(func=deploy_views)


drop_viewdata_parser = subparsers.add_parser('drop_viewdata',
                                               help='drop all views and all view data\n'
                                                    'use with caution, only for testing')
drop_viewdata_parser.set_defaults(func=drop_viewdata)



def get_database(name_or_uri):
    import couchdbkit
    if '/' in name_or_uri:
        return couchdbkit.Database(name_or_uri)
    else:
        return couchdbkit.Server().get_or_create_db(name_or_uri)

with_database = [
    push_parser,
    deploy_views_parser,
    drop_viewdata_parser,
]

for item in with_database:
    item.add_argument('database', type=get_database)


