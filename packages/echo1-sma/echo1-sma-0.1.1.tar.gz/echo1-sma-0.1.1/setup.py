# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['echo1_sma']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'echo1-sma',
    'version': '0.1.1',
    'description': 'Streaming moving average in python.',
    'long_description': '# echo1-sma\nStreaming moving average in python.\n\n## Installation\n```sh\npip install echo1-sma\n```\n\n## Getting Started\n```python\nfrom echo1_sma.echo1_sma import StreamingMovingAverage\n```',
    'author': 'Michael Mohamed',
    'author_email': 'michael.mohamed@echo1.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/e1-io/echo1-geopix',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.2',
}


setup(**setup_kwargs)
