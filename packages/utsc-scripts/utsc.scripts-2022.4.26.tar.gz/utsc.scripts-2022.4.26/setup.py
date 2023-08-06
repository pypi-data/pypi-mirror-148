# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['scripts']

package_data = \
{'': ['*']}

install_requires = \
['prompt-toolkit>=3.0.19',
 'pydantic>=1.9.0',
 'pyquery>=1.4.0',
 'requests>=2.20.0',
 'rich>=10.7.0',
 'utsc.core']

entry_points = \
{'console_scripts': ['utsc.scripts = utsc.scripts.__main__:cli']}

setup_kwargs = {
    'name': 'utsc.scripts',
    'version': '2022.4.26',
    'description': 'a collection of scripts and one-off tools',
    'long_description': None,
    'author': 'Alex Tremblay',
    'author_email': 'alex.tremblay@utoronto.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
