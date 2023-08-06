# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['ptext']
setup_kwargs = {
    'name': 'ptext',
    'version': '1.1.0',
    'description': 'Makes printing effect (ptext.printing("your text", delay_not_necessary))',
    'long_description': None,
    'author': 'TimoXBeR',
    'author_email': 'bertim20102@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.0,<4.0',
}


setup(**setup_kwargs)
