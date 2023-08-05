# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mapaction',
 'mapaction.libs',
 'mapaction.modules.templates',
 'mapaction.scripts']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.4,<0.5.0',
 'packaging>=21.3,<22.0',
 'requests>=2.27.1,<3.0.0',
 'shellingham>=1.4.0,<2.0.0',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['mapaction = mapaction.cli:run']}

setup_kwargs = {
    'name': 'mapaction',
    'version': '0.1.8',
    'description': '',
    'long_description': None,
    'author': 'Hugh Loughrey',
    'author_email': 'hloughrey@mapaction.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
