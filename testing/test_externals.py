import pytest
import mock
import restkit
from couchdb_compose import externals
from couchdb_compose import composer

UNDERSCORE = {
    'name': 'underscore',
    'url': 'http://underscorejs.org/underscore.js',
}


def test_make_cache(tmpdir):
    cache = externals.make_cache(tmpdir)

    assert cache.check(dir=1)
    assert cache.dirpath() == tmpdir
    assert cache.join('README.txt').check()


def test_download_external(tmpdir, monkeypatch):

    externals.maybe_download_external(UNDERSCORE, tmpdir)
    assert tmpdir.join('underscore.js').check()
    assert tmpdir.join('.completed').check()

    monkeypatch.setattr(restkit,
                        'request',
                        mock.Mock(side_effect=RuntimeError()))

    externals.maybe_download_external(UNDERSCORE, tmpdir)


def test_add_external_commonjs(tmpdir):
    tmpdir.join('underscore.js').write('test')

    comp = composer.Composer(tmpdir, {})
    assert 'underscore' not in comp.doc

    externals.add_external(comp, UNDERSCORE, tmpdir)
    assert 'underscore' in comp.doc
    assert '_attachments' not in comp.doc
    underscore_attachment = dict(UNDERSCORE, attachment='js/underscore.js')

    del comp.doc['underscore']
    externals.add_external(comp, underscore_attachment, tmpdir)
    assert 'underscore' not in comp.doc
    assert 'js/underscore.js' in comp.doc['_attachments']
 
    underscore_withpath = dict(UNDERSCORE, path= ['foo', 'bar'])
   
    del comp.doc['_attachments']

    externals.add_external(comp, underscore_withpath, tmpdir)
    assert 'underscore' not in comp.doc
    assert comp.doc['foo']['bar'] == 'test'
