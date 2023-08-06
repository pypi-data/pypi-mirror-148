# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['debiased_spatial_whittle']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.1.2,<4.0.0', 'numpy>=1.21.5,<2.0.0', 'scipy>=1.7.3,<2.0.0']

setup_kwargs = {
    'name': 'debiased-spatial-whittle',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'arthur',
    'author_email': 'ahw795@qmul.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://arthurpgb.pythonanywhere.com/sdw',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
