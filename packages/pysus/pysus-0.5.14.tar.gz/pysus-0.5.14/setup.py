# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysus',
 'pysus.demography',
 'pysus.online_data',
 'pysus.preprocessing',
 'pysus.tests',
 'pysus.tests.test_data',
 'pysus.utilities',
 'pysus.utilities.c-src']

package_data = \
{'': ['*'], 'pysus': ['Notebooks/*', 'Notebooks/.ipynb_checkpoints/*']}

install_requires = \
['cffi>=1.0.0',
 'colorcet==3.0.0',
 'dask==2022.4.0',
 'datashader==0.13.0',
 'dbfread==2.0.7',
 'elasticsearch==8.1.2',
 'facets-overview==1.0.0',
 'fastparquet==0.8.1',
 'folium==0.12.1',
 'gdal==3.4.1',
 'geobr==0.1.10',
 'geocoder==1.38.1',
 'geopandas==0.7.0',
 'georasters',
 'pandas==1.4.2',
 'pandasql==0.7.3',
 'pyarrow==7.0.0',
 'requests==2.27.1',
 'scipy==1.8.0',
 'tqdm==4.64.0',
 'wget==3.2',
 'xarray==2022.3.0']

setup_kwargs = {
    'name': 'pysus',
    'version': '0.5.14',
    'description': "Tools for dealing with Brazil's Public health data",
    'long_description': None,
    'author': 'Flavio Codeco Coelho',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fccoelho/PySUS',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
