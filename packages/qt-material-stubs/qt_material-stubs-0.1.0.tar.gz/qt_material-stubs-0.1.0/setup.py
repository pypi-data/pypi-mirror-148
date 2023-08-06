# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qt_material-stubs']

package_data = \
{'': ['*'],
 'qt_material-stubs': ['resources/*', 'resources/logo/*', 'resources/source/*']}

setup_kwargs = {
    'name': 'qt-material-stubs',
    'version': '0.1.0',
    'description': 'Stubs for qt-material.',
    'long_description': '# qt_material-stubs\n\n## Installation\n\n```\npip install qt_material-stubs\n```\n\n## Style Guidelines\n\nFollow the same style guidelines as [typeshed](https://github.com/python/typeshed/blob/master/CONTRIBUTING.md).\n',
    'author': '忘忧北萱草',
    'author_email': 'wybxc@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
