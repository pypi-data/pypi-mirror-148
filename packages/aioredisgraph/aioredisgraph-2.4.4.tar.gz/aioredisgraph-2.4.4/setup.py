# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aioredisgraph']

package_data = \
{'': ['*']}

install_requires = \
['aioredis>=2.0.1,<3.0.0',
 'hiredis>=2.0.0,<3.0.0',
 'prettytable>=2.1.0,<3.0.0']

setup_kwargs = {
    'name': 'aioredisgraph',
    'version': '2.4.4',
    'description': 'Async RedisGraph Python Client',
    'long_description': '[![license](https://img.shields.io/github/license/RedisGraph/redisgraph-py.svg)](https://github.com/Arzenon/aioredisgraph-py)\n[![CircleCI](https://circleci.com/gh/RedisGraph/redisgraph-py/tree/master.svg?style=svg)](https://circleci.com/gh/RedisGraph/redisgraph-py/tree/master)\n[![PyPI version](https://badge.fury.io/py/redisgraph.svg)](https://badge.fury.io/py/redisgraph)\n[![GitHub issues](https://img.shields.io/github/release/RedisGraph/redisgraph-py.svg)](https://github.com/RedisGraph/redisgraph-py/releases/latest)\n[![Codecov](https://codecov.io/gh/RedisGraph/redisgraph-py/branch/master/graph/badge.svg)](https://codecov.io/gh/RedisGraph/redisgraph-py)\n[![Known Vulnerabilities](https://snyk.io/test/github/RedisGraph/redisgraph-py/badge.svg?targetFile=pyproject.toml)](https://snyk.io/test/github/RedisGraph/redisgraph-py?targetFile=pyproject.toml)\n[![Total alerts](https://img.shields.io/lgtm/alerts/g/RedisGraph/redisgraph-py.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/RedisGraph/redisgraph-py/alerts/)\n\n# aioredisgraph-py\n[![Forum](https://img.shields.io/badge/Forum-RedisGraph-blue)](https://forum.redis.com/c/modules/redisgraph)\n[![Discord](https://img.shields.io/discord/697882427875393627?style=flat-square)](https://discord.gg/gWBRT6P)\n\nAsynchronous fork of [RedisGraph python client](https://github.com/RedisGraph/redisgraph-py/)\n\n\n## Example: Using the Python Client\n\n```python\nimport asyncio\nfrom aioredisgraph import Node, Edge, Graph, Path\n\n\nasync def main():\n   url = \'redis://localhost:6379\'\n\n   redis_graph = Graph(\'social\', url)\n\n   john = Node(label=\'person\', properties={\'name\': \'John Doe\', \'age\': 33, \'gender\': \'male\', \'status\': \'single\'})\n   redis_graph.add_node(john)\n\n   japan = Node(label=\'country\', properties={\'name\': \'Japan\'})\n   redis_graph.add_node(japan)\n\n   edge = Edge(john, \'visited\', japan, properties={\'purpose\': \'pleasure\'})\n   redis_graph.add_edge(edge)\n\n   await redis_graph.commit()\n\n   query = """MATCH (p:person)-[v:visited {purpose:"pleasure"}]->(c:country)\n               RETURN p.name, p.age, v.purpose, c.name"""\n\n   result = await redis_graph.query(query)\n\n   # Print resultset\n   result.pretty_print()\n\n   # Use parameters\n   params = {\'purpose\': "pleasure"}\n   query = """MATCH (p:person)-[v:visited {purpose:$purpose}]->(c:country)\n               RETURN p.name, p.age, v.purpose, c.name"""\n\n   result = await redis_graph.query(query, params)\n\n   # Print resultset\n   result.pretty_print()\n\n   # Use query timeout to raise an exception if the query takes over 10 milliseconds\n   result = await redis_graph.query(query, params, timeout=10)\n\n   # Iterate through resultset\n   for record in result.result_set:\n      person_name = record[0]\n      person_age = record[1]\n      visit_purpose = record[2]\n      country_name = record[3]\n\n   query = """MATCH p = (:person)-[:visited {purpose:"pleasure"}]->(:country) RETURN p"""\n\n   result = await redis_graph.query(query)\n\n   # Iterate through resultset\n   for record in result.result_set:\n      path = record[0]\n      print(path)\n\n   # All done, remove graph.\n   await redis_graph.delete()\n\n\nif __name__ == \'__main__\':\n   asyncio.run(main())\n```\n\n## Installing\n\n### Install official release\n\n```\npip install aioredisgraph\n```\n### Install latest release (Aligned with AioRedisGraph master)\n\n```\npip install git+https://github.com/Arzenon/aioredisgraph-py.git@master\n```\n\n### Install for development in env\n\n1. Create a virtualenv to manage your python dependencies, and ensure it\'s active.\n   ```virtualenv -v venv; source venv/bin/activate```\n\n2. Install [pypoetry](https://python-poetry.org/) to manage your dependencies.\n   ```pip install poetry```\n\n3. Install dependencies.\n   ```poetry install```\n\n[tox](https://tox.readthedocs.io/en/latest/) runs all code linters as its default target.\n',
    'author': 'Arzenon',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
