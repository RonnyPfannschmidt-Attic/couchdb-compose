from __future__ import print_function
import io
import restkit
import zipfile

README="""\
This Directory is used to cache couchdb composer externals,
it can be deleted to refresh the cache
"""

def make_cache(path):
    cache = path.ensure('.couchdb-compose-external-cache', dir=1)
    cache.join('README.txt').write(README)

    return cache


def download_external(external, path):
    url = external['url']
    print(' * download', url)

    resp = restkit.request(url, follow_redirect=True)

    path.join(url.split('/')[-1]).write(resp.body_string(), 'wb')
    path.ensure('.completed')


def maybe_download_external(external, path):
    if not path.join('.completed').check():
        download_external(external, path)


def add_external(composer, external, path):
    filename = external['url'].split('/')[-1]
    attachment = external.get('attachment')
    unpack = external.get('unpack')
    content = path.join(filename).read()
    
    if unpack:
        fp = io.BytesIO(content)
        zipfp = zipfile.ZipFile(fp)
        names = zipfp.namelist()
        for item in unpack:
            sourcename = item['from']
            #XXX hack for zipfile prefix
            for name in names:
                if name.endswith('/' + sourcename):
                    content = zipfp.read(name)
                    break
            else:
                print(' !', sourcename, 'not found')
            info = composer.add_attachment(item['to'], content)
            info.update(
                url = external.get('url'),
                name = external.get('name'),
            )


    elif attachment:
        info = composer.add_attachment(attachment, content)
        info.update(
            url = external.get('url'),
            name = external.get('name'),
        )
    else:
        composer.push(
            external.get('path', [external['name']]),
            content)


def include_externals(composer):
    externals = composer.getlist('externals')
    if not externals:
        return

    cache = make_cache(composer.path)


    for external in externals:
        path = cache.ensure(external['name'], dir=1)
        maybe_download_external(external, path)
        add_external(composer, external, path)

