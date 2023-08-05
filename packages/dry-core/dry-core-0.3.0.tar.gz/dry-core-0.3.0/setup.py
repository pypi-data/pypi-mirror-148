# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dry_core',
 'dry_core.exceptions',
 'dry_core.operations',
 'dry_core.selectors',
 'dry_core.services',
 'dry_core.utils']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.22,<0.23', 'pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'dry-core',
    'version': '0.3.0',
    'description': '',
    'long_description': '# Dry-core\n\n`dry-core` is core package of `dry-*` package series. Main goal \nis to minimize and power up code, make it clear and easy supportable.\n\nDocumentation will be available soon.\n',
    'author': 'Илья Маркевич',
    'author_email': 'samuray21x@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
