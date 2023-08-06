# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsw_scrapy', 'jsw_scrapy.pipelines', 'jsw_scrapy.spiders']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'fake-useragent>=0.1.11,<0.2.0',
 'jsw-nx>=1.0.87,<2.0.0',
 'psutil>=5.9.0,<6.0.0',
 'ruamel.yaml>=0.17.21,<0.18.0']

setup_kwargs = {
    'name': 'jsw-scrapy',
    'version': '1.0.1',
    'description': 'Jsw for scrapy.',
    'long_description': '# jsw-scrapy\n> Jsw for scrapy.\n\n## installation\n```shell\npip install jsw-scrapy -U\n```\n\n## usage\n```python\nimport jsw_scrapy as nx\n\n## common methods\nnx.includes([1,2,3], 2) # => True\n```\n',
    'author': 'feizheng',
    'author_email': '1290657123@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://js.work',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
