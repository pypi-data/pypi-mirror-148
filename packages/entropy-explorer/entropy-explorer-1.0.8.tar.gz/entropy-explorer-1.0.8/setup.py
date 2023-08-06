# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['entropy',
 'entropy.hedging',
 'entropy.layouts',
 'entropy.marketmaking',
 'entropy.marketmaking.orderchain',
 'entropy.oracles',
 'entropy.oracles.ftx',
 'entropy.oracles.market',
 'entropy.oracles.pythnetwork',
 'entropy.oracles.stub',
 'entropy.simplemarketmaking']

package_data = \
{'': ['*']}

install_requires = \
['Rx>=3.2.0,<4.0.0',
 'jsons>=1.6.1,<2.0.0',
 'numpy>=1.22.1,<2.0.0',
 'pandas>=1.4.1,<2.0.0',
 'pyserum>=0.5.0a0,<0.6.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'requests>=2.27.1,<3.0.0',
 'rxpy-backpressure>=1.0.0,<2.0.0',
 'solana>=0.21.0,<0.22.0',
 'websocket-client>=1.2.1,<2.0.0',
 'zstandard>=0.17.0,<0.18.0']

setup_kwargs = {
    'name': 'entropy-explorer',
    'version': '1.0.8',
    'description': 'Python integration for https://entropy.trade',
    'long_description': 'Python API for Entropy Market\n\nGet Started\n\n```\nmake setup\n```\n\nExamples in notebooks\n\n```\ncd notebooks\njupyter notebooks\n```\n\nRun a simple marketmaker\n\n```\ncd entropy\npython simplemarketmaker.py\n```\n\nInstall via pip\n\n```\npip install entropy-explorer\n```\n',
    'author': 'thiccythot',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://entropy.trade',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.11',
}


setup(**setup_kwargs)
