# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['continual',
 'continual.python',
 'continual.python.cli',
 'continual.python.cli.tests',
 'continual.python.common',
 'continual.python.sdk',
 'continual.python.sdk.templates',
 'continual.python.utils',
 'continual.rpc',
 'continual.rpc.graphql',
 'continual.rpc.management',
 'continual.rpc.management.v1',
 'continual.rpc.rpc']

package_data = \
{'': ['*'],
 'continual.python': ['examples/bank_marketing/*',
                      'examples/kickstarter/*',
                      'extras/*']}

install_requires = \
['click==8.0.4',
 'cron-descriptor>=1.2.24,<2.0.0',
 'fsspec>=0.8.5,<0.9.0',
 'gitpython>=3.1.7,<4.0.0',
 'google-cloud-storage>=1.33.0,<2.0.0',
 'grpcio>=1.27.1,<2.0.0',
 'grpcio_status>=1.31.0,<2.0.0',
 'halo>=0.0.30,<0.0.31',
 'humanize>=2.5.0,<3.0.0',
 'pandas-gbq>=0.14.1,<0.15.0',
 'pandas>=1.0.1,<2.0.0',
 'pytz>=2020.5,<2021.0',
 'pyyaml>=5.4,<6.0',
 'requests==2.23.0',
 'rich>=9.13.0,<10.0.0',
 'sqlparse>=0.4.2,<0.5.0',
 'tabulate>=0.8.6,<0.9.0',
 'toml>=0.10.2,<0.11.0',
 'tqdm>=4.54.1,<5.0.0',
 'typer==0.4.0',
 'yamale>=4.0.0,<5.0.0']

entry_points = \
{'console_scripts': ['continual = continual.python.cli.cli:cli']}

setup_kwargs = {
    'name': 'continual',
    'version': '0.5.41',
    'description': 'Operational AI for the Modern Data Stack',
    'long_description': '# Python CLI and SDK for Continual\n\nContinual is an operational AI for the modern data stack. Learn more at\nhttps://continual.ai.\n\n## Getting Started\n\nTo install the Continual CLI and SDK run:\n\n```\npip3 install continual\n```\n',
    'author': 'Continual',
    'author_email': 'support@continual.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
