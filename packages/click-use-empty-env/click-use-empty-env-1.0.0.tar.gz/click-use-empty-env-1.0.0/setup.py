# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['click_use_empty_env']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.0']

setup_kwargs = {
    'name': 'click-use-empty-env',
    'version': '1.0.0',
    'description': 'A very small addon package to click that restores the ability to use empty values from env variables.',
    'long_description': None,
    'author': 'Ulrich Petri',
    'author_email': 'python@ulo.pe',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ulope/click-use-emty-env',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
