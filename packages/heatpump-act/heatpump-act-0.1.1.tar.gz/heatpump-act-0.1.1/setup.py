# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['act']

package_data = \
{'': ['*']}

install_requires = \
['croniter',
 'python-crontab',
 'python-dotenv',
 'pytz',
 'structlog',
 'tqdm',
 'typer',
 'urllib3']

setup_kwargs = {
    'name': 'heatpump-act',
    'version': '0.1.1',
    'description': 'Scripts to act on a heatpump',
    'long_description': '# myforest/heatpump-act\n\nA set of scripts to determine what actions we should request the heatpump to perform.\n\nThis is based on tooling [David Bowen](https://github.com/MyForest) built from 2019-09-30 which has been used to control an Ecodan 14kW.\n\nA lot of discussion relating to this can be found on the [OpenEnergyMonitor Community](https://community.openenergymonitor.org/search?q=%40myforest%20%23heatpump).',
    'author': 'David Bowen',
    'author_email': 'david@myforest.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MyForest/heatpump-act',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2',
}


setup(**setup_kwargs)
