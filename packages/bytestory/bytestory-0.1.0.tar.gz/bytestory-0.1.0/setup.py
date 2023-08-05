# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bytestory']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bytestory',
    'version': '0.1.0',
    'description': 'Unpacking from bytes and packing into bytes, with an object interface.',
    'long_description': "# ByteStory\n\nUnpacking from bytes and packing into bytes, with an object interface.\n\n## Install\n\n```commandline\npip install bytestory\n```\n\n## Usage\n\nUnpacking from bytes\n\n```python\nimport bytestory\n\nclass OneByte(bytestory.ByteStory):\n    a = bytestory.Char\n\none_byte = OneByte(b'\\x11')\n\nassert one_byte.a == 0x11\n```\n\nPacking into bytes\n\n```python\nimport bytestory\n\nclass OneByte(bytestory.ByteStory):\n    a = bytestory.Char\n\none_byte = OneByte(a=0x11)\n\nassert one_byte.pack() == b'\\x11'\n```\n\nMore examples at [tests/test_bytestory.py](tests/test_bytestory.py).\n",
    'author': 'Xu Siyuan',
    'author_email': 'inqb@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/no1xsyzy/bytestory',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
