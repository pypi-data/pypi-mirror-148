# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['switchconfig', 'switchconfig.example_template_dir']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0.1',
 'arrow>=1.1.1',
 'hier-config>=2.1.0',
 'ipdb>=0.13.9',
 'netaddr>=0.8.0',
 'paramiko>=2.7.2',
 'pexpect>=4.8.0',
 'prompt-toolkit>=3.0.19',
 'pydantic>=1.9.0',
 'rich>=10.7.0',
 'utsc.core']

entry_points = \
{'console_scripts': ['utsc.switchconfig = utsc.switchconfig.__main__:cli']}

setup_kwargs = {
    'name': 'utsc.switchconfig',
    'version': '2022.4.26',
    'description': 'A tool to easily provision switches on the bench',
    'long_description': None,
    'author': 'Alex Tremblay',
    'author_email': 'alex.tremblay@utoronto.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
