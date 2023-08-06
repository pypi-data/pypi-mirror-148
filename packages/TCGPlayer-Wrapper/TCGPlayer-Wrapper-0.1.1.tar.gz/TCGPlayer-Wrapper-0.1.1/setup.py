# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tcg_player', 'tcg_player.schemas']

package_data = \
{'': ['*']}

install_requires = \
['dataclasses-json>=0.5.7,<0.6.0',
 'ratelimit>=2.2.1,<3.0.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'tcgplayer-wrapper',
    'version': '0.1.1',
    'description': '',
    'long_description': '# TCGPlayer Wrapper\n\n[![PyPI - Python](https://img.shields.io/pypi/pyversions/TCGPlayer-Wrapper.svg?logo=PyPI&label=Python&style=flat-square)](https://pypi.python.org/pypi/TCGPlayer-Wrapper/)\n[![PyPI - Status](https://img.shields.io/pypi/status/TCGPlayer-Wrapper.svg?logo=PyPI&label=Status&style=flat-square)](https://pypi.python.org/pypi/TCGPlayer-Wrapper/)\n[![PyPI - Version](https://img.shields.io/pypi/v/TCGPlayer-Wrapper.svg?logo=PyPI&label=Version&style=flat-square)](https://pypi.python.org/pypi/TCGPlayer-Wrapper/)\n[![PyPI - License](https://img.shields.io/pypi/l/TCGPlayer-Wrapper.svg?logo=PyPI&label=License&style=flat-square)](https://opensource.org/licenses/GPL-3.0)\n\n[![Black](https://img.shields.io/badge/Black-Enabled-000000?style=flat-square)](https://github.com/psf/black)\n[![Flake8](https://img.shields.io/badge/Flake8-Enabled-informational?style=flat-square)](https://github.com/PyCQA/flake8)\n[![Pre-Commit](https://img.shields.io/badge/Pre--Commit-Enabled-informational?logo=pre-commit&style=flat-square)](https://github.com/pre-commit/pre-commit)\n\n[![Github - Contributors](https://img.shields.io/github/contributors/Buried-In-Code/TCGPlayer-Wrapper.svg?logo=Github&label=Contributors&style=flat-square)](https://github.com/Buried-In-Code/TCGPlayer-Wrapper/graphs/contributors)\n\n[![Github Action - Code Analysis](https://img.shields.io/github/workflow/status/Buried-In-Code/TCGPlayer-Wrapper/Code%20Analysis?logo=Github-Actions&label=Code-Analysis&style=flat-square)](https://github.com/Buried-In-Code/TCGPlayer-Wrapper/actions/workflows/code-analysis.yaml)\n[![Github Action - Testing](https://img.shields.io/github/workflow/status/Buried-In-Code/TCGPlayer-Wrapper/Testing?logo=Github-Actions&label=Tests&style=flat-square)](https://github.com/Buried-In-Code/TCGPlayer-Wrapper/actions/workflows/testing.yaml)\n\nA [Python](https://www.python.org/) wrapper for the [TCGPlayer](https://tcgplayer.com) API.\n\n## Installation\n\n### Poetry\n\n```bash\n$ poetry add TCGPlayer-Wrapper\n```\n\n### Local Setup\n\n1. Make sure you have [Python](https://python.org/) installed: `python --version`\n2. Make sure you have [Poetry](https://python-poetry.org/) installed: `poetry --version`\n3. Clone the repo: `git clone https://github.com/<Username>/TCGPlayer-Wrapper`\n4. Install the project and its dependencies via poetry: `poetry install`\n\n## Example Usage\n\n```python\nfrom tcg_player.service import TCGPlayer\nfrom tcg_player.sqlite_cache import SQLiteCache\n\nsession = TCGPlayer(client_id="Client ID", client_secret="Client Secret", cache=SQLiteCache())\n\n# List Games\nresults = session.list_categories()\nfor game in results:\n    print(f"{game.category_id} | {game.display_name}")\n\n# List Magic: the Gathering Expansions\nresults = session.list_category_groups(category_id=1)\nfor expansion in results:\n    print(f"{expansion.group_id} | [{expansion.abbreviation}] - {expansion.name}")\n\n# Get Product and Prices via product ID\nresult = session.product(product_id=257275)\nprices = session.product_prices(product_id=257275)\nprint(f"{result.clean_name} ${prices.market_price:,.2f}")\n```\n\n## Socials\n\n[![Social - Discord](https://img.shields.io/badge/Discord-The--DEV--Environment-7289DA?logo=Discord&style=flat-square)](https://discord.gg/nqGMeGg)\n',
    'author': 'Buried-In-Code',
    'author_email': 'BuriedInCode@tuta.io',
    'maintainer': 'Buried-In-Code',
    'maintainer_email': 'BuriedInCode@tuta.io',
    'url': 'https://github.com/Buried-In-Code/TCGPlayer-Wrapper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
