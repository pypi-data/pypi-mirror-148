# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['amplified']
setup_kwargs = {
    'name': 'amplified',
    'version': '0.0.0',
    'description': 'Amplify your Python developer experience',
    'long_description': None,
    'author': 'Jeroen Schot',
    'author_email': 'jeroenschot@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6.2',
}


setup(**setup_kwargs)
