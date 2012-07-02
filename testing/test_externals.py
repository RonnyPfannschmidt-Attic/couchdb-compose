import pytest
import mock
import restkit
from couchdb_compose import externals

def test_make_cache(tmpdir):
    cache = externals.make_cache(tmpdir)

    assert cache.check(dir=1)
    assert cache.dirpath() == tmpdir
    assert cache.join('README.txt').check()


def test_download_external(tmpdir, monkeypatch):
    underscore = {
        'name': 'underscore',
        'url': 'http://underscorejs.org/underscore.js',
    }

    externals.maybe_download_external(underscore, tmpdir)
    assert tmpdir.join('underscore.js').check()
    assert tmpdir.join('.completed').check()

    monkeypatch.setattr(restkit,
                        'request',
                        mock.Mock(side_effect=RuntimeError()))

    externals.maybe_download_external(underscore, tmpdir)
    
