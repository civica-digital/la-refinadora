#!/usr/bin/env python

from distutils.core import setup

setup(
    name='Validadora',
    version='0.1',
    description='Validate datasets',
    author='Miguel Salazar & Miguel Angel Gordian',
    author_email='mike@civiva.digital & miguel.angel@civica.digital',
    url='https://github.com/civica-digital/refinadora',

    package_dir={
        'validadora': 'src/validadora',
        'validadora.manager': 'src/validadora/manager',
        'validadora.util': 'src/validadora/util'
    },
    package_data={
        'validadora': ['templates/*.html',
            'static/*/*/*',
            'static/*/*'],
    },
    entry_points={
        'validadora':[
            'server = validadora:run'
        ]
    },
    packages=['validadora', 'validadora.manager','validadora.util']
)
