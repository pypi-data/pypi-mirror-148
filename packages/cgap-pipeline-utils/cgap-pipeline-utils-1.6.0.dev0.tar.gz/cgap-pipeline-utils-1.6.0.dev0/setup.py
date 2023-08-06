# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pipeline_utils', 'pipeline_utils.lib']

package_data = \
{'': ['*']}

install_requires = \
['awscli>=1.22.15,<2.0.0',
 'boto3>=1.20.15,<2.0.0',
 'dcicutils>=3.2.0,<4.0.0',
 'magma-suite>=0.2.1,<0.3.0']

entry_points = \
{'console_scripts': ['pipeline_utils = pipeline_utils.__main__:main']}

setup_kwargs = {
    'name': 'cgap-pipeline-utils',
    'version': '1.6.0.dev0',
    'description': 'Repository implementing utilities for deploying pipelines that implement the CGAP-Pipeline specification.',
    'long_description': None,
    'author': 'CGAP Team',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dbmi-bgm/cgap-pipeline-utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<3.10',
}


setup(**setup_kwargs)
