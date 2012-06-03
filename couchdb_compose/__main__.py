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
    import couchdbkit
    server = couchdbkit.Server()
    db = server.get_or_create_db(args.database)
    print('storing to', db)
    db.save_doc(composer.doc, force=True)


push_parser = subparsers.add_parser('push')
push_parser.set_defaults(func=push)
push_parser.add_argument('database')


def main():
    args = parser.parse_args()
    composer = Composer(py.path.local(args.path))
    composer.run_actions(actions)
    args.func(args, composer)


if __name__ == '__main__':
    main()
