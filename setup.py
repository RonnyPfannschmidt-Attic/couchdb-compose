from setuptools import setup

setup(
    name='couchdb-compose',
    get_version_from_scm=True,
    description='library to compose couchapps',
    
    install_requires=[
        'coffeescript',
        'couchdbkit',
        'Jinja2',
        'Hamlish-Jinja',
        'MarkupSafe',
    ],
    
    setup_requires=[
        'hgdistver',
    ],
)
