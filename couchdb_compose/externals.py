import restkit

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

    resp = restkit.request(url)
    path.join(url.split('/')[-1]).write(resp.body_string())
    path.ensure('.completed')


def maybe_download_external(external, path):
    if not path.join('.completed').check():
        download_external(external, path)


def add_external(composer, external, path):
    filename = external['url'].split('/')[-1]
    attachment = external.get('attachment')
    content = path.join(filename).read()
    if attachment:
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
        maybe_download_external(external, cache)
        add_external(composer, external, path)

