# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['weatherchart']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'weatherchart',
    'version': '0.1.1',
    'description': 'Generate chart image based on 7 day forecast form a given location',
    'long_description': '# weatherchart\nGet a weather chart image\n',
    'author': 'pub12',
    'author_email': 'pubudu79@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pubs12/weatherchart',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
