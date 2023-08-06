# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['isitwo']

package_data = \
{'': ['*']}

install_requires = \
['boto3-type-annotations>=0.3.1,<0.4.0',
 'boto3>=1.22.0,<2.0.0',
 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['isitwo = isitwo.main:app']}

setup_kwargs = {
    'name': 'isitwo',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'pquadri',
    'author_email': 'pquadri10@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
