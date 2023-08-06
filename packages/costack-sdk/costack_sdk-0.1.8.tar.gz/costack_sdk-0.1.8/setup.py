# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['costack_sdk',
 'costack_sdk.costack_lambda',
 'costack_sdk.costack_workflow',
 'costack_sdk.costack_workflow.context',
 'costack_sdk.integrations']

package_data = \
{'': ['*']}

install_requires = \
['config>=0.5.1,<0.6.0', 'slack-sdk>=3.15.2,<4.0.0']

setup_kwargs = {
    'name': 'costack-sdk',
    'version': '0.1.8',
    'description': 'the sdk to support lambda workflows and seamless integrations',
    'long_description': None,
    'author': 'perseus.yang',
    'author_email': 'perseus.yang@getcostack.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
