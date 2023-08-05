# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['smartonnx', 'smartonnx.entities']

package_data = \
{'': ['*'], 'smartonnx': ['templates/*']}

install_requires = \
['Jinja2>=3.1.1,<4.0.0',
 'click==8.0.4',
 'cogapp>=3.3.0,<4.0.0',
 'cookiecutter>=1.7.3,<2.0.0',
 'onnx>=1.11.0,<2.0.0',
 'protobuf>=3.20.1,<4.0.0',
 'requests>=2.27.1,<3.0.0',
 'rich>=12.0.1,<13.0.0',
 'toml>=0.10.2,<0.11.0',
 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['smartonnx = smartonnx.main:app']}

setup_kwargs = {
    'name': 'smartonnx',
    'version': '0.1.0',
    'description': 'Tool to convert a ONNX model to Cairo smart contract.',
    'long_description': '# smartonnx\n\nTool to convert a ONNX model to Cairo smart contract\n',
    'author': 'Fran Algaba',
    'author_email': 'f.algaba.work@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.11,<3.9',
}


setup(**setup_kwargs)
