# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src']

package_data = \
{'': ['*']}

install_requires = \
['flake9>=3.8.3,<4.0.0']

setup_kwargs = {
    'name': 'lgg',
    'version': '0.1.0',
    'description': 'A simple yet fancy logger for Python scripts',
    'long_description': '# python-logger\nA simple yet fancy logger for Python scripts\n',
    'author': 'Ayoub Assis',
    'author_email': 'assis.ayoub@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/blurry-mood/python-logger',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
