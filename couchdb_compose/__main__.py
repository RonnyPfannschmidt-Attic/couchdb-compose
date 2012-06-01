import py
import yaml
from couchdb_compose.composer import Composer, actions

def main(argv=None):
    composer = Composer(py.path.local())
    for action in actions:
        print action
        action(composer)
    print yaml.dump(composer.doc)

main()
