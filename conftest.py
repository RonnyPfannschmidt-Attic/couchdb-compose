import py
examplesdir = py.path.local(__file__).dirpath().join('examples')

def pytest_funcarg__composer(request):
    from couchdb_compose.composer import Composer
    return Composer(examplesdir.join('streamsapp'))
