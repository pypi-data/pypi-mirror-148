# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spw', 'spw.config']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=36.0.2,<37.0.0',
 'lmdb>=1.3.0,<2.0.0',
 'pyperclip>=1.8.2,<2.0.0']

entry_points = \
{'console_scripts': ['spw = spw.main:app']}

setup_kwargs = {
    'name': 'spw',
    'version': '1.7.0',
    'description': 'store and retrieve passwords securely all while being scriptable!',
    'long_description': '### About\n\nspw is an application that stores and retrieves passwords in a secure manner. spw is designed to be quick, light on resources/dependencies, and command line/script driven.\n\nPasswords are stored in an encrypted format using PKCS1_OAEP encryption. This means you use a public and private key to encrypt and decrypt items stored within the store. This is a secure method of password storage and there is virtually no chance someone (including yourself) can view decrypted passwords without the private key.\n\nspw is intended to provide a secure mechanism to store (and more importantly retrieve) passwords. spw\'s command-line interface allows easy integration into openbox\'s keyboard shortcut functionality (or similar tools). spw provides an easy mechanism for copying a password to the clipboard (e.g. C+A+j will copy the gmail junk account\'s password to your clipboard).\n\n\n### Requiremnts\n\n- python3\n\n\n### Install\n\nWe recommend using [pipx](https://github.com/pypa/pipx) to install spw: `pipx install spw`. You can also install via pip: `pip install --user spw`.\n\ncryptik uses a config file to store your setup. This file contains information where your secure database is stored and the private key to use. You can grab the sample config file from  [spw/example/spw.ini.template](https://gitlab.com/drad/spw/-/blob/master/examples/spw.ini.template) and place it at `~/.config/spw/spw.ini`.\n\n\n### Usage\n\nAfter spw has been installed and setup you can use it as follows:\n- add a key: `spw --add-key="abc" --value="123"`\n- get a key: `spw --get-key="abc"`\n  + note that the password retrieved is not show but rather placed on your clipboard so you can easily paste it somewhere ;-)\n\nYou can find more on the usage by calling help: `spw --help`\n\n\n### Notes\n\n- to avoid special character issues in keys/values, surround them with single (\') or double (") quotes. If your password has single quotes in it, surround it with double quotes. If your password has double quotes in it, surround it with single quotes.\n- you can use spw to store any string for quick retrieval, a commonly used URL, a base64 encoded picture, a snippet of code, etc.\n\n\n### More Info\n\n- [Wiki](https://g.dradux.com/dradux/spw/wikis/home)\n- [Issues/Enhancements](https://g.dradux.com/dradux/spw/issues)\n- [bandit](https://github.com/PyCQA/bandit)\n- [flake8](https://gitlab.com/pycqa/flake8)\n',
    'author': 'David Rader',
    'author_email': 'sa@adercon.com',
    'maintainer': 'David Rader',
    'maintainer_email': 'sa@adercon.com',
    'url': 'https://gitlab.com/drad/spw',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
