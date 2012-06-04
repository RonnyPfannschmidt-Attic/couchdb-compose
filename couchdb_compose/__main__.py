from __future__ import print_function
import py
import json
from couchdb_compose.composer import Composer, actions


from argparse import ArgumentParser
parser = ArgumentParser(prog='couchdb-compose')


parser.add_argument('--path', nargs='?', default=py.std.os.getcwd())
subparsers = parser.add_subparsers()


def show(args, composer):
    json.dump(composer.doc.keys(), py.std.sys.stdout, indent=2)


show_parser = subparsers.add_parser('show')
show_parser.set_defaults(func=show)


def push(args, composer):
    if args.deploy_views:
        deploy_views(args, composer)
    
    import couchdbkit
    server = couchdbkit.Server()
    db = server.get_or_create_db(args.database)
    print('storing to', db, composer.doc['_id'])
    # we copy here to avoid _rev being set
    db.save_doc(composer.doc.copy(), force_update=True)


push_parser = subparsers.add_parser('push', help='stores the composed doc to the db')
push_parser.set_defaults(func=push)
push_parser.add_argument('database')
push_parser.add_argument('--deploy-views', action='store_true',
                         help='deploy views before pushing',
                        )


def deploy_views(args, composer):
    import couchdbkit
    server = couchdbkit.Server()
    db = server.get_or_create_db(args.database)
    newid = composer.doc['_id'] + ":view-deploy"
    print('storing to', db, newid)
    newdoc = dict(composer.doc, _id=newid)
    view_basename = newid.split('/', 1)[1] + '/'
    print(view_basename)
    
    db.save_doc(newdoc, force_update=True)

    for name, view in newdoc.get('views', {}).items():
        if isinstance(view, dict) and 'map' in view:
            print('request view', name, view)
            list(db.view(view_basename+name, limit=1, stale='update_after'))
            break # stop after the first
    py.std
    found = True
    while found:
        py.std.time.sleep(.1)
        tasks = server.active_tasks()
        found = False
        for task in tasks:
            if task['database'] == db.dbname and \
               task['design_document'] == newdoc['_id']:
                found = True
                print('progress', task['progress'])
    print('done')
                

deploy_views_parser = subparsers.add_parser('deploy_views', 
                                            help='stores the ddoc to a different id and updates all views, '
                                                 'usefull for view updates before a push')
deploy_views_parser.set_defaults(func=deploy_views)
deploy_views_parser.add_argument('database')

def main(argv=None, composer=None):
    args = parser.parse_args(argv)
    composer = composer or Composer(py.path.local(args.path))
    composer.run_actions(actions)
    args.func(args, composer)


if __name__ == '__main__':
    main()
