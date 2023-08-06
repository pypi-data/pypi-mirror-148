# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyusage', 'usage']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'pyusage',
    'version': '0.1.4',
    'description': '',
    'long_description': '# usage',
    'author': 'PyUsage Team',
    'author_email': 'packages@pyusage.org',
    'maintainer': 'Balaji Veeramani',
    'maintainer_email': 'bveeramani@berkeley.edu',
    'url': 'https://pyusage.org',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
