# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rhealsf']

package_data = \
{'': ['*']}

install_requires = \
['rhealpix-geo>=0.3.0,<0.4.0']

setup_kwargs = {
    'name': 'rhealpix-sf',
    'version': '0.4.1',
    'description': 'This library contains functions for evaluating Simple Feature relations between DGGS Cells and sets of these.',
    'long_description': None,
    'author': 'david-habgood',
    'author_email': 'david.habgood@surroundaustralia.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
