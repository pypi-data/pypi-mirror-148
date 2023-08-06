# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['msg2po']

package_data = \
{'': ['*']}

install_requires = \
['configparser>=5.2.0',
 'natsort>=6.2.1,<7',
 'polib>=1.1.1',
 'python-dateutil>=2.8.2',
 'ruamel.yaml>=0.17.21']

entry_points = \
{'console_scripts': ['bgforge-config = msg2po.bgforge-config:main',
                     'dir2msgstr = msg2po.dir2msgstr:main',
                     'file2msgstr = msg2po.file2msgstr:main',
                     'file2po = msg2po.file2po:main',
                     'msgmerge-female = msg2po.msgmerge:main',
                     'po2file = msg2po.po2file:main',
                     'resave-po = msg2po.resave-po:main',
                     'unpoify = msg2po.unpoify:main']}

setup_kwargs = {
    'name': 'msg2po',
    'version': '1.1.0',
    'description': 'A set of helper tools to convert Fallout 1/2 MSG and WeiDU TRA into GNU gettext PO and back',
    'long_description': '# MSG2PO\n\nThis is a set of tools to convert Fallout 1/2 MSG and WeiDU TRA into GNU gettext PO and back, used in BGforge [translation system](https://tra.bgforge.net/). Ask questions [here](https://forums.bgforge.net/viewforum.php?f=9).\n\n## Usage\n\n```\ngit clone https://github.com/BGforgeNet/msg2po.git\ncd msg2po\npip3 install -r requirements.txt\n./msg2po -h\n```\n',
    'author': 'BGforge',
    'author_email': 'dev@bgforge.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/BGforgeNet/msg2po',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2',
}


setup(**setup_kwargs)
