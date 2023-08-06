# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['solace', 'solace.cli']

package_data = \
{'': ['*']}

install_requires = \
['Cerberus>=1.3.4,<2.0.0',
 'Jinja2>=3.1.1,<4.0.0',
 'PyInquirer>=1.0.3,<2.0.0',
 'arrow>=1.2.2,<2.0.0',
 'loguru>=0.6.0,<0.7.0',
 'pyaml>=21.10.1,<22.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'pygogo>=1.3.0,<2.0.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'requests>=2.27.1,<3.0.0',
 'starlette>=0.19.0,<0.20.0',
 'typer[all]>=0.4.1,<0.5.0',
 'uvicorn>=0.17.6,<0.18.0',
 'watchgod>=0.8.2,<0.9.0']

entry_points = \
{'console_scripts': ['solace = solace.cli:cli']}

setup_kwargs = {
    'name': 'solace',
    'version': '0.1.14',
    'description': 'A Modern Framework for Building Python Web Apps',
    'long_description': '# Solace\n\nSolace is a next generation web framework for Python3, inspired by Koa.\n\n## Goals\n\n- make a framework that enables truly re-usable code\n- provide a "common sense" approach to building web apps\n- enable rapid development and deployment using best practices\n- solve the problem first, then write the code\n\n## Concepts\n\n- request flows can be crafted\n\n### Made from Open Source Projects\n\n- Poetry\n- Starlette\n- Typer\n- Pydantic\n- Loguru\n- python-dotenv\n- Jinja2\n- Arrow\n',
    'author': 'Dan Sikes',
    'author_email': 'dansikes7@gmail.com',
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
