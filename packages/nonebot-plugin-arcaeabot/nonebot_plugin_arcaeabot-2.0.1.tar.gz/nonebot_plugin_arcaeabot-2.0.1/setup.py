# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_arcaeabot',
 'nonebot_plugin_arcaeabot.AUA',
 'nonebot_plugin_arcaeabot.AUA.schema',
 'nonebot_plugin_arcaeabot.AUA.schema.api',
 'nonebot_plugin_arcaeabot.AUA.schema.api.v5',
 'nonebot_plugin_arcaeabot.handlers',
 'nonebot_plugin_arcaeabot.image_generator']

package_data = \
{'': ['*'],
 'nonebot_plugin_arcaeabot': ['assets/*',
                              'assets/diff/*',
                              'assets/font/*',
                              'assets/grade/*',
                              'assets/ptt/*',
                              'assets/recent/*',
                              'database/*']}

install_requires = \
['Pillow>=8.3.1',
 'httpx>=0.20.0,<1.0.0',
 'nonebot-adapter-onebot>=2.0.0-beta.1,<=2.0.0-beta.2',
 'nonebot2>=2.0.0-beta.1,<=2.0.0-beta.2',
 'peewee>=3.14.4',
 'ruamel.yaml>=0.17.2,<0.18.0',
 'tqdm>=4.1.0,<5.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-arcaeabot',
    'version': '2.0.1',
    'description': 'An arcaea plugin for nonebot2. ( A cross platform Python async bot framework. )',
    'long_description': None,
    'author': 'SEAFHMC',
    'author_email': 'soku_ritsuki@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
