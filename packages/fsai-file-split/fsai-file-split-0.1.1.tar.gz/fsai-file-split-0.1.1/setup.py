# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fsai_file_split', 'fsai_file_split.split_libs']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0']

entry_points = \
{'console_scripts': ['file-split = fsai_file_split.main:app']}

setup_kwargs = {
    'name': 'fsai-file-split',
    'version': '0.1.1',
    'description': 'Split a json or jsonl file into different chunks.',
    'long_description': '# fsai-file-split\nSplit a json or jsonl file into different chunks.\n\n## Installation \n```shell\npip install fsai-file-split\n```\n\n## Usage\n```shell\nfile-split \\\n--input_file_path ./tests/data/test.jsonl \\\n--save_to_dir /tmp/output/ \\\n--output_file_name test.jsonl \\\n--split_by number_of_buckets \\\n--chunk_size 10\n```',
    'author': 'Michael Mohamed',
    'author_email': 'michael@foundationstack.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fsai-dev/fsai-file-split',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
