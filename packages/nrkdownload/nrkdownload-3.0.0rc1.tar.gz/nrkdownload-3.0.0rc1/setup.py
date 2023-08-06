# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nrkdownload']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'ffmpeg-python>=0.2.0,<0.3.0',
 'halo>=0.0.31,<0.0.32',
 'loguru>=0.6.0,<0.7.0',
 'pydantic>=1.9.0,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'typer[all]>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['nrkdownload = nrkdownload.cli:app']}

setup_kwargs = {
    'name': 'nrkdownload',
    'version': '3.0.0rc1',
    'description': '',
    'long_description': None,
    'author': 'Martin Høy',
    'author_email': 'marhoy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
