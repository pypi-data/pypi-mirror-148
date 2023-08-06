# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['itslive']

package_data = \
{'': ['*']}

install_requires = \
['Shapely>=1.8.1,<2.0.0',
 'matplotlib>=3.5.1,<4.0.0',
 'pyproj>=3.3.1,<4.0.0',
 's3fs>=2022.3.0,<2023.0.0',
 'xarray>=2022.3.0,<2023.0.0',
 'zarr>=2.11.3,<3.0.0']

setup_kwargs = {
    'name': 'itslive',
    'version': '0.1.1',
    'description': 'Python client for ITSLIVE gralcier velocity data',
    'long_description': None,
    'author': 'betolink',
    'author_email': 'luis.lopez@nsidc.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
