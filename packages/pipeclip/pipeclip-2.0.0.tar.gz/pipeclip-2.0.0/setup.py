# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pipeclip', 'pipeclip.lib']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.2,<9.0.0',
 'colorama>=0.4.4,<0.5.0',
 'pybedtools>=0.9.0,<0.10.0',
 'pysam>=0.19.0,<0.20.0',
 'rpy2>=3.5.1,<4.0.0']

entry_points = \
{'console_scripts': ['pipeclip = pipeclip.main:runPipeClip']}

setup_kwargs = {
    'name': 'pipeclip',
    'version': '2.0.0',
    'description': 'PIPELINE FOR CLIP SEQ DATA',
    'long_description': None,
    'author': 'Chang Ye',
    'author_email': 'yech1990@gmail.com',
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
