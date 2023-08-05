# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gtkspellcheck']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'gtkspellcheck',
    'version': '0.0.0',
    'description': 'A placeholder for `pygtkspellcheck` which is imported as `gtkspellcheck`.',
    'long_description': 'This package exists just to reserve the name `gtkspellcheck`.\n',
    'author': 'Maximilian Köhl',
    'author_email': 'mail@koehlma.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/koehlma/pygtkspellcheck',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
