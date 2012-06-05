import py
import sys
from couchdb_compose import cli
from couchdb_compose.composer import Composer, actions
from docopt import docopt

def doc_main(args, composer=None):
    print args
    composer = composer or Composer(py.path.local(args['--path']))
    composer.run_actions(actions)
    cli._dispatch(args, composer)

def main(argv=None, composer=None):
    if argv is None:
        argv = sys.argv[1:]
    args = docopt(cli.__doc__, argv=argv)
    return doc_main(args, composer)
if __name__ == '__main__':
    main()
