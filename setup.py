from setuptools import setup

setup(
    name='couchdb-compose',
    get_version_from_scm=True,
    description='library to compose couchapps',
    
    entry_points={
        'console_scripts':[
            'couchdb-compose = couchdb_compose.__main__:main',
        ]},

    install_requires=[
        'coffeescript',
        'couchdbkit',
        'Jinja2',
        'Hamlish-Jinja',
        'MarkupSafe',
        'py',
    ],
    
    setup_requires=[
        'hgdistver',
    ],
)
