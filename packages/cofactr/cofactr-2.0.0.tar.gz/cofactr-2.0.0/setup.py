# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cofactr']

package_data = \
{'': ['*']}

install_requires = \
['urllib3>=1.26.9,<2.0.0']

setup_kwargs = {
    'name': 'cofactr',
    'version': '2.0.0',
    'description': 'Client library for accessing Cofactr data.',
    'long_description': '# Cofactr\n\nPython client library for accessing Cofactr.\n\n## Example\n\n```python\nfrom cofactr.graph import GraphAPI\nfrom cofactr.cursor import first\n\ng = GraphAPI()\n\ncursor = g.get_products(\n    query="esp32",\n    fields="id,aliases,labels,statements{spec,assembly},offers",\n    batch_size=10,  # Data is fetched in batches of 10 products.\n    limit=10,  # `list(cursor)` would have at most 10 elements.\n    external=False,\n)\n\ndata = first(cursor, 2)\n\n# To send to web app.\nresponse = {\n    "data": data,\n    # To get the next 10 after the 2 in `data`.\n    "paging": cursor.paging,\n}\n```\n',
    'author': 'Noah Trueblood',
    'author_email': 'noah@cofactr.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Cofactr/cofactr-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
