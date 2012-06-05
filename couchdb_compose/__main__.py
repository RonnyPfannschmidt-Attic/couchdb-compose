import py
from couchdb_compose.cli import parser
from couchdb_compose.composer import Composer, actions

def main(argv=None, composer=None):
    args = parser.parse_args(argv)
    composer = composer or Composer(args.path)
    composer.run_actions(actions)
    args.func(args, composer)


if __name__ == '__main__':
    main()
