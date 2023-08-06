# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djp_sepa', 'djp_sepa.fints', 'djp_sepa.migrations']

package_data = \
{'': ['*'],
 'djp_sepa': ['locale/de_DE/LC_MESSAGES/*', 'templates/djp_sepa/fints/*']}

install_requires = \
['django-localflavor>=3.1,<4.0', 'django-payments>=1.0.0,<2.0.0']

extras_require = \
{'fints': ['fints>=3.1.0,<4.0.0', 'svgwrite>=1.4.2,<2.0.0']}

setup_kwargs = {
    'name': 'django-payments-sepa',
    'version': '1.2.dev1',
    'description': 'django-payments provider for SEPA',
    'long_description': None,
    'author': 'Dominik George',
    'author_email': 'dominik.george@teckids.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://edugit.org/AlekSIS/libs/django-payments-sepa',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
