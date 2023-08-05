# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rfkit', 'rfkit.io', 'rfkit.math']

package_data = \
{'': ['*']}

install_requires = \
['h5py', 'numpy', 'pandas', 'scikit-rf>=0.22.0,<0.23.0', 'scipy']

setup_kwargs = {
    'name': 'pyrfkit',
    'version': '1.1.0',
    'description': 'Python RF Kit built on scikit-rf.',
    'long_description': None,
    'author': 'Adam Page',
    'author_email': 'adam.page@samtec.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://bitbucket.org/samteccmd/pyrfkit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
