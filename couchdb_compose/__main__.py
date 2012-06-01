from __future__ import print_function
import py
import json
from couchdb_compose.composer import Composer, actions

from argparse import ArgumentParser
parser = ArgumentParser()

parser.add_argument('path', nargs='?', default=py.std.os.getcwd())


def main():
    args = parser.parse_args()
    composer = Composer(py.path.local(args.path))
    for action in actions:
        print('start', action.__name__, file=py.std.sys.stderr)
        action(composer)
    json.dump(composer.doc.keys(), py.std.sys.stdout, indent=2)

main()
