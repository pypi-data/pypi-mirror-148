# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['payroll_1c']
setup_kwargs = {
    'name': 'payroll-1c',
    'version': '0.2',
    'description': 'Parse 1C Payrolls XML file',
    'long_description': None,
    'author': 'Dmitry Voronin',
    'author_email': 'dimka665@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/odoo-ru/payroll-1c',
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
