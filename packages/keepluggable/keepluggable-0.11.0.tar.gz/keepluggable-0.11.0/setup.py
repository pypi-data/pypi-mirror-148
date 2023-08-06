# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['keepluggable',
 'keepluggable.storage_file',
 'keepluggable.storage_metadata',
 'keepluggable.web',
 'keepluggable.web.pyramid']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.0.0,<8.1.0',
 'bag>=5.0.0',
 'colander>=1.0.0,<2.0.0',
 'kerno>=0.7.0',
 'pillow-heif>=0.1.0,<0.2.0',
 'sqlalchemy']

extras_require = \
{'aws': ['awscli>=1.22.0,<1.23.0', 'boto3>=1.20.0,<1.21.0']}

setup_kwargs = {
    'name': 'keepluggable',
    'version': '0.11.0',
    'description': 'Manage storage of images and other files, with metadata.',
    'long_description': None,
    'author': 'Nando Florestan',
    'author_email': 'nandoflorestan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nandoflorestan/keepluggable',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
