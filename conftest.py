import py
import yaml
examplesdir = py.path.local(__file__).dirpath().join('examples')


def pytest_funcarg__composer(request):
    from couchdb_compose.composer import Composer
    s = examplesdir.join('streamsapp')
    with s.join('couchdb-compose.yml').open() as fd:
        d = yaml.load(fd)
    return Composer(examplesdir.join('streamsapp'), d)
