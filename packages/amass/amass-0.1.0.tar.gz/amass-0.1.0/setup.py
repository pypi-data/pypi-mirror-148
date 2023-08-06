# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['amass']
setup_kwargs = {
    'name': 'amass',
    'version': '0.1.0',
    'description': 'Vendor libraries from cdnjs',
    'long_description': None,
    'author': 'James Meakin',
    'author_email': 'amass@jmsmkn.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
