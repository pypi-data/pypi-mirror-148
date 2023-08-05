# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['task_flows']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.35,<2.0.0',
 'alert-msgs>=0.0.4,<0.0.5',
 'psycopg2>=2.9.3,<3.0.0']

setup_kwargs = {
    'name': 'task-flows',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Dan',
    'author_email': 'kelleherjdan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
