# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dynafile']

package_data = \
{'': ['*']}

install_requires = \
['atomicwrites>=1.4.0,<2.0.0', 'sortedcontainers>=2.4.0,<3.0.0']

extras_require = \
{'filter': ['filtration>=2.3.0,<3.0.0']}

setup_kwargs = {
    'name': 'dynafile',
    'version': '0.1.2',
    'description': 'NoSQLDB following the Dynamo concept, but for a filebased embedded db.',
    'long_description': '> Consider the project as a proof of concept! Definitely not production ready!\n\n# Dynafile\n\nEmbedded pure Python NoSQL database following DynamoDB concepts.\n\n```bash\n\npip install dynafile\n\n# with string filter support using filtration\n\npip install "dynafile[filter]"\n\n# bloody edge\n\npip install git+https://github.com/eruvanos/dynafile.git\npip install filtration\n\n```\n\n## Overview\n\nDynafile stores items within partitions, which are stored as separate files. Each partition contains a SortedDict\nfrom `sortedcontainers` which are sorted by the sort key attribute.\n\nDynafile does not implement the interface or functionality of DynamoDB, but provides familiar API patterns.\n\nDifferences:\n\n- Embedded, file based\n- No pagination\n\n## Features\n\n- persistence\n- put item\n- get item\n- delete item\n- scan - without parameters\n- query - starts_with\n- query - index direction\n- query - filter\n- scan - filter\n- batch writer\n- atomic file write\n- event stream hooks (put, delete)\n- TTL\n\n## Roadmap\n\n- GSI - global secondary index\n- update item\n- batch get\n- thread safeness\n- LSI - local secondary index\n- split partitions\n- parallel scans - pre defined scan segments\n- transactions\n- optimise disc load time (cache partitions in memory, invalidate on file change)\n- conditional put item\n- improve file consistency (options: acidfile)\n\n## API\n\n```python\nfrom dynafile import *\n\n# init DB interface\ndb = Dynafile(path=".", pk_attribute="PK", sk_attribute="SK")\n\n# put items\ndb.put_item(item={"PK": "user#1", "SK": "user#1", "name": "Bob"})\ndb.put_item(item={"PK": "user#1", "SK": "role#1", "TYPE": "sender"})\ndb.put_item(item={"PK": "user#2", "SK": "user#2", "name": "Alice"})\n\n# more performant batch operation\nwith db.batch_writer() as writer:\n    db.put_item(item={"PK": "user#3", "SK": "user#3", "name": "Steve"})\n    db.delete_item(key={"PK": "user#3", "SK": "user#3"})\n\n# retrieve items\nitem = db.get_item(key={\n    "PK": "user#1",\n    "SK": "user#1"\n})\n\n# query item collection by pk\nitems = list(db.query(pk="user#1"))\n\n# scan full table\nitems = list(db.scan())\n\n# add event stream listener to retrieve item modification\ndef print_listener(event: Event):\n    print(event.action)\n    print(event.old)\n    print(event.new)\n\n\ndb.add_stream_listener(print_listener)\n\n```\n\n### Filter\n\n`query` and `scan` support filter, you can provide callables as filter like lambda expressions.\n\nAnother option are [filtration](https://pypi.org/project/filtration/) expressions.\n\n* Equal ("==")\n* Not equal ("!=")\n* Less than ("<")\n* Less than or equal ("<=")\n* Greater than (">")\n* Greater than or equal (">=")\n* Contains ("in")\n    * RHS must be a list or a Subnet\n* Regular expression ("=~")\n    * RHS must be a regex token\n\nExamples:\n\n* `SK =~ /^a/` - SK starts with a\n* `SK == 1` - SK is equal 1\n* `SK == 1` - SK is equal 1\n* `nested.a == 1` - accesses nested structure `item.nested.a`\n\n### TTL - Time To Live\n\nTTL provides the option to expire items on read time (get, query, scan).\n\n```python\nimport time\nfrom dynafile import *\n\ndb = Dynafile(path=".", pk_attribute="PK", sk_attribute="SK", ttl_attribute="ttl")\n\nitem = {"PK": "1", "SK": "2", "ttl": time.time() - 1000} # expired ttl\ndb.put_item(item=item)\n\nlist(db.scan()) # -> []\n\n```\n\n## Architecture\n\n![architecture.puml](https://github.com/eruvanos/dynafile/blob/9bf858e83ff5761cffca10a18b4554fe5ba2d3c7/architecture.png?raw=true)\n\n### File Structure\n\n```text\n\n--- ROOT ---\n./db/\n\n--- MAIN DB ---\n\n|- meta.json - meta information\n|- _partitions/\n    |- <hash>/\n        |- data.pickle - Contains partition data by sort key (SortedDict)\n        |- lsi-attr1.pickle - Contains partition data by lsi attr (SortedDict)\n\n--- GSI ---\n|- _gsi-<gsi-name>/\n    |- _partitions/\n        |- <hash>/\n            |- data.pickle - Contains partition data by sort key (SortedDict)\n\n```',
    'author': 'Maic Siemering',
    'author_email': 'maic@siemering.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eruvanos/dynafile',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
