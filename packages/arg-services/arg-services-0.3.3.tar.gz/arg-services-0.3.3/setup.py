# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arg_services',
 'arg_services.graph',
 'arg_services.graph.v1',
 'arg_services.mining',
 'arg_services.mining.v1',
 'arg_services.nlp',
 'arg_services.nlp.v1',
 'arg_services.retrieval',
 'arg_services.retrieval.v1']

package_data = \
{'': ['*']}

install_requires = \
['grpcio-reflection>=1.32.0,<2.0.0',
 'grpcio>=1.32.0,<2.0.0',
 'protobuf>=3.15.8,<4.0.0']

setup_kwargs = {
    'name': 'arg-services',
    'version': '0.3.3',
    'description': 'gRPC definitions for microservice-based argumentation machines',
    'long_description': '# Argumentation Microservices\n\nDocumentation is hosted at the [Buf Schema Registry](https://buf.build/recap/arg-services/docs).\n',
    'author': 'Mirko Lenz',
    'author_email': 'info@mirko-lenz.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://recap.uni-trier.de',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
