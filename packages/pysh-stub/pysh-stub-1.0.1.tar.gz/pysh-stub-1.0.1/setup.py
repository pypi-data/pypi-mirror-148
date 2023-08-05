# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysh']

package_data = \
{'': ['*']}

install_requires = \
['ideas>=0.0.37,<0.0.38',
 'tomlkit>=0.10.0,<0.11.0',
 'typer[all]>=0.4.0,<0.5.0',
 'typing-extensions>=4.2.0,<5.0.0']

entry_points = \
{'console_scripts': ['pysh = pysh:main']}

setup_kwargs = {
    'name': 'pysh-stub',
    'version': '1.0.1',
    'description': 'A bunch of shortcuts to simplify scripting in python',
    'long_description': None,
    'author': 'Stanislav Zmiev',
    'author_email': 'szmiev2000@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
