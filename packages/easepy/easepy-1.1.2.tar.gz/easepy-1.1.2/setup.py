# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['easepy']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.2,<2.0.0', 'pyproj>=3.3.0,<4.0.0']

setup_kwargs = {
    'name': 'easepy',
    'version': '1.1.2',
    'description': 'Python package for working with EASE grids.',
    'long_description': '# easepy\n\n![test-main](https://github.com/karl-nordstrom/easepy/actions/workflows/python-test-main.yml/badge.svg)\n![coverage-main](https://img.shields.io/codecov/c/github/karl-nordstrom/easepy)\n![license](https://img.shields.io/github/license/karl-nordstrom/easepy)\n\nA python package for working with EASE grids in geodetic coordinates.\nThe documentation is available at https://easepy.readthedocs.io/en/latest/.\nThe code is available at https://github.com/karl-nordstrom/easepy.\n\nInstallation\n------------\n\n    pip install easepy\n\nExample usage\n-------------\n\n    import easepy\n    ease = easepy.EaseGrid(resolution_m=25000, projection="Global")\n    # Fetch grid cell centroids\n    grid_lats, grid_lons = ease.geodetic_grid\n    # Find corresponding cell indices for particular location(s)\n    ease_indices, _ = ease.geodetic2ease(lat=46.7, lon=132.1)\n\nAuthors:\n\n- Karl Nordstrom (<karl.am.nordstrom@gmail.com>)\n- Giorgio Savastano (<giorgiosavastano@gmail.com>)\n\nPlease use github issues to make bug reports and request new functionality. Contributions are always welcome.\n',
    'author': 'Karl Nordstrom',
    'author_email': 'karl.am.nordstrom@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
