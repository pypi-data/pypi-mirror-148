# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ccc_cli']

package_data = \
{'': ['*']}

install_requires = \
['tabulate>=0.8.9,<0.9.0']

entry_points = \
{'console_scripts': ['cccls = ccc_cli.ccc6_print_task_runs:main']}

setup_kwargs = {
    'name': 'ccc-cli',
    'version': '0.1.3',
    'description': 'Command line utility for Carbon Copy Cloner',
    'long_description': '',
    'author': 'Xinyuan Chen',
    'author_email': '45612704+tddschn@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tddschn/ccc-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
