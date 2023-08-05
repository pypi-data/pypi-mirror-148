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
    'version': '0.1.9',
    'description': 'CLI for managing some MapAction tasks',
    'long_description': '<p align="center">\n  <a href="https://mapaction.org/">\n      <img alt="MapAction" src="https://qb19onvfjt-flywheel.netdna-ssl.com/wp-content/themes/mapaction/images/logo.svg" width="210" />\n  </a>\n</p>\n<h1 align="center">\nMapAction CLI\n</h1>\n\nCLI tool for managing MapAction tasks.\n\n## Getting Started\n\nRequirements:\n\n- [Poetry](https://python-poetry.org/)\n\n### Development\n\n```bash\npoetry shell\npoetry install\npre-commit install\npython -m mapaction -v\n```\n\n### Build\n\n```bash\npoetry shell\npoetry build\n```\n\n### Generate requirements.txt\n\n```bash\npoetry shell\npoetry export -f requirements.txt --output requirements.txt\n```\n\n### Creating a release\n\n```bash\npoetry shell\npoetry version <patch, minor, major>\ngit commit -m "Release v<Version>"\n// After Merge\ngit tag -a v<Version> -m "release v<Version>"\n```\n',
    'author': 'Hugh Loughrey',
    'author_email': 'hloughrey@mapaction.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mapaction/mapaction-cli',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
