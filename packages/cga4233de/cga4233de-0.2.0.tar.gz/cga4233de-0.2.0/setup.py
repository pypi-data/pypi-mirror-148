# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cga4233de']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['disable_firewall = cga4233de:disable_firewall',
                     'recent_calls = cga4233de:recent_calls']}

setup_kwargs = {
    'name': 'cga4233de',
    'version': '0.2.0',
    'description': 'Library to interact with the CGA4233DE router, distributed by Vodafone Germany',
    'long_description': "# CGA4233DE\n\nThis is a python library to interact with the CGA4233DE router, as provided by Vodafone Germany.\n\n## References\n\n- [tiberiucorbu's writeup on authenticating with CGA4233DE](https://gist.github.com/tiberiucorbu/a51c81b82b5196ac002c52ac6f39987f)\n",
    'author': 'no92',
    'author_email': 'no92.mail@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zebradil/cga4233de',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
