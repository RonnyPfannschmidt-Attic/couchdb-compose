from __future__ import print_function
import py
import json
from couchdb_compose.composer import Composer, actions


from argparse import ArgumentParser
parser = ArgumentParser()


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
    print('storing to', db)
    db.save_doc(composer.doc, force=True)


push_parser = subparsers.add_parser('push', help='stores the composed doc to the db')
push_parser.set_defaults(func=push)
push_parser.add_argument('database')
push_parser.add_argument('--deploy-views', action='store_true',
                         help='deploy views before pushing',
                        )


def deploy_views(args, composer):

    server = couchdbkit.Server()
    db = server.get_or_create_db(args.database)
    print('storing to', db)
    newid = composer.doc['_id'] + ":view-deploy"
    newdoc = dict(composer.doc, _id=newid)
    view_basename = newid.split('/', 1)[1] + '/'

    
    db.save_doc(newdoc, force=True)

    for view in newdoc['views']:
        list(db.view(view_basename+view, limit=1))


deploy_views_parser = subparsers.add_parser('deploy_views', help='stores the ddoc to a different id and updates all views, usefull for view updates before a push')
deploy_views_parser.set_defaults(func=deploy_views)

def main():
    args = parser.parse_args()
    composer = Composer(py.path.local(args.path))
    composer.run_actions(actions)
    args.func(args, composer)


if __name__ == '__main__':
    main()
