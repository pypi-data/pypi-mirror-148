# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rabbitmq_provider',
 'rabbitmq_provider.hooks',
 'rabbitmq_provider.operators',
 'rabbitmq_provider.sensors']

package_data = \
{'': ['*']}

install_requires = \
['apache-airflow>=1.10', 'pika>=1.2.0,<2.0.0', 'whippet>=0.3.2,<0.4.0']

entry_points = \
{'apache_airflow_provider': ['provider_info = '
                             'rabbitmq_provider.__init__:get_provider_info']}

setup_kwargs = {
    'name': 'airflow-provider-rabbitmq',
    'version': '0.6.0',
    'description': 'A RabbitMQ provider for Apache Airflow',
    'long_description': None,
    'author': 'Tes Engineering',
    'author_email': 'engineering@tesglobal.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
