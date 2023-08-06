# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['soldata']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.3,<2.0.0', 'pandas>=1.4.2,<2.0.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'solana-data-scraper',
    'version': '0.0.0',
    'description': 'Python library for scraping blockchain data from Bitquery',
    'long_description': '',
    'author': 'thiccythot',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://app.friktion.fi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
