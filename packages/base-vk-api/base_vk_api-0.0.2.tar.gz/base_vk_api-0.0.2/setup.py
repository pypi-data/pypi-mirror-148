# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['base_vk_api']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.2,<2.0.0', 'requests']

setup_kwargs = {
    'name': 'base-vk-api',
    'version': '0.0.2',
    'description': 'Base VK API client based on Pydantic models',
    'long_description': '# vrslev/base-vk-api\n\n📦 Archived!\n\nThis is tiny VK API client. It uses [Requests](https://github.com/psf/requests) and [Pydantic](https://github.com/samuelcolvin/pydantic).\n',
    'author': 'Lev Vereshchagin',
    'author_email': 'mail@vrslev.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/vrslev/base-vk-api',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
