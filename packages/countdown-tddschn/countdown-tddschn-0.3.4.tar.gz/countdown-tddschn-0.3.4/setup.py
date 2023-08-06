# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['countdown_tddschn', 'countdown_tddschn.bin']

package_data = \
{'': ['*']}

install_requires = \
['pync>=2.0.3,<3.0.0', 'python-daemon>=2.3.0,<3.0.0', 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['scd = countdown_tddschn.bin.simple_countdown:app']}

setup_kwargs = {
    'name': 'countdown-tddschn',
    'version': '0.3.4',
    'description': '',
    'long_description': '',
    'author': 'Xinyuan Chen',
    'author_email': '45612704+tddschn@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tddschn/countdown-tddschn',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
