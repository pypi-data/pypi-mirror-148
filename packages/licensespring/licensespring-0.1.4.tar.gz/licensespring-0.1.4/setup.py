# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['licensespring', 'licensespring.api']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'licensespring',
    'version': '0.1.4',
    'description': 'LicenseSpring Python Library',
    'long_description': '# LicenseSpring Python Library\n\nThe LicenseSpring Python library provides convenient access to the LicenseSpring API from\napplications written in the Python language.\n',
    'author': 'Toni Sredanović',
    'author_email': 'toni@licensespring.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://licensespring.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
