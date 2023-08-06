# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lespy',
 'lespy.confs',
 'lespy.converters',
 'lespy.core',
 'lespy.http',
 'lespy.http.request',
 'lespy.http.response',
 'lespy.server']

package_data = \
{'': ['*']}

install_requires = \
['pyfunctools>=0.5.1,<0.6.0']

setup_kwargs = {
    'name': 'lespy',
    'version': '0.1.0',
    'description': 'A small and robust micro Python framework for building simple and solid web apps.',
    'long_description': None,
    'author': 'Natan Santos',
    'author_email': 'natansantosapps@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
