# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['notion_cli_py',
 'notion_cli_py.client',
 'notion_cli_py.configure',
 'notion_cli_py.operations',
 'notion_cli_py.utils']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.4.0,<0.5.0',
 'requests>=2.27.1,<3.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['notion-cli = notion_cli_py.cli:main']}

setup_kwargs = {
    'name': 'notion-cli-py',
    'version': '1.0.1',
    'description': 'NotionCLI - The CLI tool for Notion.co (https://www.notion.so/ja-jp/product).',
    'long_description': '## NotionCLI\n\nNotionCLI - The CLI tool for Notion.co (https://www.notion.so/ja-jp/product).\n\n## Installation\n\n* To install NotionCLI with pip, run: `pip install notion-cli-py`\n\n## How to use\n\n### Create Integration\n\nTo use the notion api, you need to create an integration. Please create it [here](https://www.notion.so/my-integrations).\n\n![image-notion1](./image-notion1.png)\n\n![image-notion2](./image-notion2.png)\n\n### Setup\n\nAfter installation, you are required to create config file first.\nPlease run following command.\n\n```\n$ notion-cli configure set\n```\n\nThen you need to put your integration information about the following questions.\n\n```\nAre you sure to create config file in /Users/hiratatomonori/.notion_cli? [y/N]: # Type \'y\'.\ninput config label name: # Type your integration name (e.g. "NotionCLI").\ninput token for NotionCLI: # Type your integration token.\nDo you want to set label (LABEL NAME) to current label? [y/N]: # Type \'y\' (if this is your first setting).\n```\n\nPlease run following command and check that the configuration is completed properly.\n\n```\n### Check if the target page has the integration that set above.\n$ notion-cli get pages ${PAGE_ID}\n```\n\nIf page information can be retrieved the minimum setup is complete.\n\n## Basic Commands\n\nFor more detailed information, run `notion-cli <command> - --help` or  `notion-cli <command> <subcommand> - --help`.\n### Get (Retrieve) Operations\n\n```\n### get pages information\n$ notion-cli get pages ${PAGE_IDS}\n\n### get pages properties\n$ notion-cli get page_properties ${PAGE_IDS} ${PROPERTY_ID}\n\n### get databases information\n$ notion-cli get databases ${DATABASE_IDS}\n\n### get blocks information\n$ notion-cli get blocks ${BLOCK_IDS}\n\n### get block children information\n$ notion-cli get block_children ${BLOCK_IDS}\n\n### get users information\n$ notion-cli get users ${USERS_IDS}\n\n### get all users information\n$ notion-cli get all_users\n```\n\n### Create Operations\n\n```\n### create pages\n$ notion-cli create pages ${PALENT_PAGE_IDS} --read-path=${YOUR_FILE_PATH}\n\n### create databases\n$ notion-cli create databases ${PALENT_PAGE_IDS} --read-path=${YOUR_FILE_PATH}\n```\n### Update Operations\n\n```\n### update pages\n$ notion-cli update pages ${PALENT_PAGE_IDS} --read-path=${YOUR_FILE_PATH}\n\n### update databases\n$ notion-cli update databases ${PALENT_PAGE_IDS} --read-path=${YOUR_FILE_PATH}\n\n### update blocks\n$ notion-cli update blocks ${PALENT_PAGE_IDS} --read-path=${YOUR_FILE_PATH}\n```\n### Delete Operations\n\n```\n### delete blocks\n$ notion-cli delete blocks ${BLOCK_IDS}\n```\n### Append Operations\n\n```\n### append block children\n$ notion-cli append block_children ${BLOCK_IDS} --read-path=${YOUR_FILE_PATH}\n```\n\n### Configure Operations\n\n```\n### set your integration information\n$ notion-cli configure set\n\n### show your integration information\n$ notion-cli configure show\n\n### switch integration\n$ notion-cli configure switch ${LABEL_NAME}\n```\n### Query Operations\n\n```\n### query databases\n$ notion-cli query databases ${YOUR_FILE_PATH}\n```\n### Search Operations\n\n```\n### search objects\n$ notion-cli search data ${YOUR_FILE_PATH}\n```\n## License\n\nLicensed under the [MIT](https://github.com/fieldflat/notion-cli-py/blob/main/LISENSE) License.\n\n## Disclaimer\n\nThis is **NOT** an official Notion product.\n',
    'author': 'Tomonori HIRATA',
    'author_email': 'tomonori4565@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fieldflat',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
