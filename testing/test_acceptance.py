import py
from couchdb_compose.composer import Composer, actions

examplesdir = py.path.local(__file__).dirpath().dirpath().join('examples')


def test_streamsapp():

    composer = Composer(examplesdir/'streamsapp')
    composer.run_actions(actions)
    
    
