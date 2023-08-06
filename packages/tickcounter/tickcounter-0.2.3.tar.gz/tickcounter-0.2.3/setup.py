# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tickcounter',
 'tickcounter.findings',
 'tickcounter.plot',
 'tickcounter.questionnaire',
 'tickcounter.statistics',
 'tickcounter.survey',
 'tickcounter.util']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.2.2',
 'pandas>=1.3.5',
 'pyyaml>=6.0',
 'scipy>=1.4.1',
 'seaborn>=0.11.2']

setup_kwargs = {
    'name': 'tickcounter',
    'version': '0.2.3',
    'description': 'A library for processing survey data',
    'long_description': 'Overview\n--------\n\n**tickcounter** is a Python package built to facilitate the process of cleaning, manipulating and analyzing questionnaire or survey related data effectively. \n\nInstallation\n------\nYou can install the latest version using `pip`.\n\n```\npip install tickcounter\n```\n\nDependencies\n----\n- python: >=3.7.1\n- pandas: >=1.3.5\n- scipy: >=1.4.1\n- matplotlib: >=3.2.2\n- seaborn: >=0.11.2\n\nUsage\n----\nDocumentation is still under development. Meanwhile, you can look at some notebook examples in the `examples` folder.\n\nA Word of Caution\n----\nThe interfaces are still unstable and are most likely to change in the near future.\n',
    'author': 'Ong Eng Kheng',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1',
}


setup(**setup_kwargs)
