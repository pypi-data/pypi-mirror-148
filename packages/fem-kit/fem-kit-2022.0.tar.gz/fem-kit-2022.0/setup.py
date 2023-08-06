# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src']

package_data = \
{'': ['*']}

install_requires = \
['typer']

setup_kwargs = {
    'name': 'fem-kit',
    'version': '2022.0',
    'description': 'Geoemtry modification and modeling tools to create and publish an industry strength numerical solver into an optimization chain, which can handle real-time data. ',
    'long_description': '# Sim-Kit / Sim-Paster /FEM - kit \n',
    'author': 'Tamás Orosz',
    'author_email': 'orosz.tamas@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tamasorosz/fem-kit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
