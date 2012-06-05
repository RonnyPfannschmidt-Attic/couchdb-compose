import sys
import py
import yaml
from docopt import docopt

from couchdb_compose import cli
from couchdb_compose.composer import Composer, actions

def doc_main(args, composer=None):
    if composer is None:
        path = py.path.local(args['--path'])
        with path.join('couchdb-compose.yml').open() as fp:
            config = yaml.load(fp)
        composer = Composer(path, config)
    composer.run_actions(actions)
    cli._dispatch(args, composer)

def main(argv=None, composer=None):
    if argv is None:
        argv = sys.argv[1:]
    args = docopt(cli.__doc__, argv=argv)
    return doc_main(args, composer)

if __name__ == '__main__':
    main()
