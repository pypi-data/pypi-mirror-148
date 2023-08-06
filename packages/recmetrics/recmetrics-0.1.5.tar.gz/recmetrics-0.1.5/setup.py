# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['recmetrics']

package_data = \
{'': ['*']}

install_requires = \
['funcsigs>=1.0.2,<2.0.0',
 'ipython>=7.18.1,<8.0.0',
 'jupyter>=1.0.0,<2.0.0',
 'matplotlib>=3.3.2,<4.0.0',
 'pandas>=1.1.3,<2.0.0',
 'plotly>=4.11.0,<5.0.0',
 'pytest-cov>=2.10.1,<3.0.0',
 'scikit-learn>=1.0.2,<2.0.0',
 'scipy>=1.5.2,<2.0.0',
 'seaborn>=0.11.0,<0.12.0',
 'twine>=4.0.0,<5.0.0']

setup_kwargs = {
    'name': 'recmetrics',
    'version': '0.1.5',
    'description': 'A library of metrics for evaluating recommender systems',
    'long_description': None,
    'author': 'Claire Longo',
    'author_email': 'longoclaire@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
