# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['useragent_classifier', 'useragent_classifier.custom_transformers']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.4,<9.0.0',
 'dash>=2.3.0,<3.0.0',
 'pandas>=1.4.1,<2.0.0',
 'plotly>=5.6.0,<6.0.0',
 'scikit-learn>=1.0.2,<2.0.0']

entry_points = \
{'console_scripts': ['useragent_classifier = '
                     'useragent_classifier:main.ua_clustering']}

setup_kwargs = {
    'name': 'useragent-classifier',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'thibaultB',
    'author_email': 'thibault.blanc@yahoo.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
