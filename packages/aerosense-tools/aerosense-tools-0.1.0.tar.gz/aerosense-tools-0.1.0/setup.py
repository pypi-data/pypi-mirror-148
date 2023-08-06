# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aerosense_tools']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aerosense-tools',
    'version': '0.1.0',
    'description': 'Functions for working with aerosense data, useful in building dashboards, analysis notebooks and digital twin services',
    'long_description': '# aerosense-tools\nFunctions for working with aerosense data, useful in building dashboards, analysis notebooks and digital twin services\n',
    'author': 'Tom Clark',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aerosense-ai/aerosense-tools',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
