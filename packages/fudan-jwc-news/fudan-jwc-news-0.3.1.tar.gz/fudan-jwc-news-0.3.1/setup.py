# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fudan_jwc_news']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2', 'requests>=2.27.1,<3.0.0', 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['jwc-news = fudan_jwc_news.jwc_news:main']}

setup_kwargs = {
    'name': 'fudan-jwc-news',
    'version': '0.3.1',
    'description': 'Read Fudan JWC news from your terminal',
    'long_description': '# fudan-jwc-news\n\n## Installation\n\n### pipx\n\n```\npipx install fudan-jwc-news\n```\n\n### pip\n\n```\npip install fudan-jwc-news\n```\n\n## Usage\n\n```\nUsage: jwc-news [OPTIONS]\n\nOptions:\n  -l, --limit INTEGER RANGE       limit the number of news  [default: 14;\n                                  x<=14]\n  -o, --output PATH               output file, default is stdout\n  -f, --force-update              do not use cache and force update\n  --install-completion [bash|zsh|fish|powershell|pwsh]\n                                  Install completion for the specified shell.\n  --show-completion [bash|zsh|fish|powershell|pwsh]\n                                  Show completion for the specified shell, to\n                                  copy it or customize the installation.\n  --help                          Show this message and exit.\n```\n',
    'author': 'Xinyuan Chen',
    'author_email': '45612704+tddschn@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tddschn/fudan-jwc-news',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
