# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['task_flows']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.35,<2.0.0',
 'alert-msgs>=0.0.4,<0.0.5',
 'docker>=5.0.3,<6.0.0',
 'psycopg2>=2.9.3,<3.0.0',
 'tqdm>=4.64.0,<5.0.0']

entry_points = \
{'console_scripts': ['create_services = task_flows.services:main']}

setup_kwargs = {
    'name': 'task-flows',
    'version': '0.1.3',
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
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
