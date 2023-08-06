# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beancount_swe']

package_data = \
{'': ['*']}

install_requires = \
['beancount>=2.3.5,<3.0.0']

setup_kwargs = {
    'name': 'beancount-swe',
    'version': '0.1.0',
    'description': 'Beancount Importer fro csv exports from Swedish banks. Supports Länsförsäkringar',
    'long_description': '# README\n\nWe help Sweden cook their books using Beancount since 2022!\n\n## Gettings stated\nIn the example folder there is a example beancount project which uses [`beancount-swe`](https://github.com/owodunni/beancount-swe) with [`fava`](https://beancount.github.io/fava/) and [`beancount`](https://beancount.github.io/) to manage personal finance from swedish banks.\n\n```\ncp examples ~/my-beancount\n```\n\n```\ncd ~/my-beancount\n```\n\nOpen `~/my-beancount/README.md` for further instructions on how to use the example project.\n\n## Development\n\nInstall:\n```\npip install poetry\n```\n\n```\npoetry install\n```\n\nBuild:\n```\npoetry build\n```\n\nTest:\n```\npoetry run pytest\n```\n\nLint:\n```\npoetry run flake8\n```\n\nFix:\n```\npoetry run black . && poetry run isort beancount-swe/ tests/\n```\n\n',
    'author': 'Alexander Poole',
    'author_email': 'alex.o.poole@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/owodunni/beancount-swe',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
