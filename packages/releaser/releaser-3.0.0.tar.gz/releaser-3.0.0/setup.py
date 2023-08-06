# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['releaser']

package_data = \
{'': ['*']}

install_requires = \
['bag>=5.0.0,<6.0.0',
 'docutils<0.18',
 'grimace>=0.1.0,<0.2.0',
 'requests',
 'wheel']

setup_kwargs = {
    'name': 'releaser',
    'version': '3.0.0',
    'description': 'Automates the process of releasing a new version of some software.',
    'long_description': None,
    'author': 'Nando Florestan',
    'author_email': 'nandoflorestan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nandoflorestan/releaser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
