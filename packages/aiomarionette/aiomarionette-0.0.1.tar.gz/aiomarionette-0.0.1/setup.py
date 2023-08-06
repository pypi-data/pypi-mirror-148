# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['aiomarionette']
setup_kwargs = {
    'name': 'aiomarionette',
    'version': '0.0.1',
    'description': 'Firefox Marionette client for asyncio',
    'long_description': None,
    'author': 'Dustin C. Hatch',
    'author_email': 'dustin@hatch.name',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
