# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rnotify', 'rnotify.lib']

package_data = \
{'': ['*']}

install_requires = \
['click-config-file>=0.6.0,<0.7.0',
 'click>=8.1.2,<9.0.0',
 'discord-webhook>=0.15.0,<0.16.0',
 'notifiers>=1.3.3,<2.0.0',
 'psutil>=5.9.0,<6.0.0',
 'pymsteams>=0.2.1,<0.3.0',
 'python-daemon>=2.3.0,<3.0.0',
 'validators>=0.18.2,<0.19.0',
 'watchdog>=2.1.7,<3.0.0',
 'watchfiles>=0.13,<0.14']

entry_points = \
{'console_scripts': ['rn = rnotify.main:cli', 'rnotify = rnotify.main:cli']}

setup_kwargs = {
    'name': 'rnotify',
    'version': '0.1.0',
    'description': 'Tracking system changes on Unix hosts and letting you know about it.',
    'long_description': None,
    'author': 'Nicholas A',
    'author_email': '@edmcboy',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
