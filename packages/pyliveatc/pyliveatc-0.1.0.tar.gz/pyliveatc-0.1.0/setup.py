# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyliveatc', 'pyliveatc.models']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.2,<9.0.0',
 'ffmpeg-python>=0.2.0,<0.3.0',
 'loguru>=0.6.0,<0.7.0',
 'lxml>=4.8.0,<5.0.0',
 'numpy>=1.22.3,<2.0.0',
 'pandas>=1.4.2,<2.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'scipy>=1.8.0,<2.0.0',
 'sounddevice>=0.4.4,<0.5.0']

setup_kwargs = {
    'name': 'pyliveatc',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'ruyyi0323',
    'author_email': 'ruyyi0323@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
