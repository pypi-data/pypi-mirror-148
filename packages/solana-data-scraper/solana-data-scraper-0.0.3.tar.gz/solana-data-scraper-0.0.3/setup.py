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
    'version': '0.0.3',
    'description': 'Python library for scraping blockchain data from Bitquery',
    'long_description': '# Scrape Solana Blockchain Data\n\nThis python library scrapes blockchain from https://bitquery.io/ from their GraphQL endpoints.\n\nThis requires you to supply your own Bitquery API token.\n\n# Setup\n\n1. Create an account at https://bitquery.io/\n2. Retrieve API Key\n3. `export BITQUERY_API_KEY=XXXXXXX`\n\n# Functionalities\n\n- Queries Bitquery for blockchain data\n- Batches queries to get around compute limits.\n- Returns output as a pandas dataframe or saves data to a csv\n',
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
