# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tickytacky']

package_data = \
{'': ['*']}

install_requires = \
['pyglet>=1.5.23,<2.0.0']

setup_kwargs = {
    'name': 'tickytacky',
    'version': '0.7.0',
    'description': 'Tickytacky pixel game maker',
    'long_description': '# Tickytacky\n\n[![tickytacky pypi shield](https://img.shields.io/pypi/v/tickytacky)](https://pypi.org/project/tickytacky/)\n\n## Description\n\nThis library aims to make it easy to make retro-style games with Pyglet.\n\n## Examples\n\nExamples can be found here, in the examples, repo:\n\n[Tickytacky Examples](https://github.com/numbertheory/tickytacky-examples)\n',
    'author': 'JP Etcheber',
    'author_email': 'jetcheber@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
