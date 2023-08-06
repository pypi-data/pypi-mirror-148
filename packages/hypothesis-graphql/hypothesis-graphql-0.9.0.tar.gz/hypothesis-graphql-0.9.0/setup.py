# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hypothesis_graphql', 'hypothesis_graphql._strategies']

package_data = \
{'': ['*']}

install_requires = \
['attrs>20.3.0,<=21.4.0',
 'graphql-core>=3.1.0,<3.3.0',
 'hypothesis>=5.8.0,<7.0']

setup_kwargs = {
    'name': 'hypothesis-graphql',
    'version': '0.9.0',
    'description': 'Hypothesis strategies for GraphQL queries and mutations',
    'long_description': '# hypothesis-graphql\n\n[![Build](https://github.com/Stranger6667/hypothesis-graphql/workflows/build/badge.svg)](https://github.com/Stranger6667/hypothesis-graphql/actions)\n[![Coverage](https://codecov.io/gh/Stranger6667/hypothesis-graphql/branch/master/graph/badge.svg)](https://codecov.io/gh/Stranger6667/hypothesis-graphql/branch/master)\n[![Version](https://img.shields.io/pypi/v/hypothesis-graphql.svg)](https://pypi.org/project/hypothesis-graphql/)\n[![Python versions](https://img.shields.io/pypi/pyversions/hypothesis-graphql.svg)](https://pypi.org/project/hypothesis-graphql/)\n[![Chat](https://img.shields.io/discord/938139740912369755)](https://discord.gg/VnxfdFmBUp)\n[![License](https://img.shields.io/pypi/l/hypothesis-graphql.svg)](https://opensource.org/licenses/MIT)\n\nHypothesis strategies for GraphQL operations. Allows you to generate arbitrary GraphQL queries for the given schema.\nIt starts with simple examples and iteratively goes to more complex ones.\n\nFor web API testing, [Schemathesis](https://github.com/schemathesis/schemathesis) provides a higher-level wrapper and can\ndetect internal server errors.\n\n## Usage\n\n`hypothesis_graphql` exposes the `from_schema` function, which takes a GraphQL schema and returns a Hypothesis strategy for\ndefined queries and mutations:\n\n```python\nfrom hypothesis import given\nfrom hypothesis_graphql import from_schema\n\nSCHEMA = """\ntype Book {\n  title: String\n  author: Author\n}\n\ntype Author {\n  name: String\n  books: [Book]\n}\n\ntype Query {\n  getBooks: [Book]\n  getAuthors: [Author]\n}\n\ntype Mutation {\n  addBook(title: String!, author: String!): Book!\n  addAuthor(name: String!): Author!\n}\n"""\n\n\n@given(from_schema(SCHEMA))\ndef test_graphql(query):\n    # Will generate samples like these:\n    #\n    # {\n    #   getBooks {\n    #     title\n    #   }\n    # }\n    #\n    # mutation {\n    #   addBook(title: "H4Z\\u7869", author: "\\u00d2"){\n    #     title\n    #   }\n    # }\n    ...\n```\n\nIt is also possible to generate queries or mutations separately with `hypothesis_graphql.queries` and `hypothesis_graphql.mutations`.\n\n### Customization\n\nTo restrict the set of fields in generated operations use the `fields` argument:\n\n```python\n@given(from_schema(SCHEMA, fields=["getAuthors"]))\ndef test_graphql(query):\n    # Only `getAuthors` will be generated\n    ...\n```\n\nIt is also possible to generate custom scalars. For example, `Date`:\n\n```python\nfrom hypothesis import strategies as st, given\nfrom hypothesis_graphql import from_schema, nodes\n\nSCHEMA = """\nscalar Date\n\ntype Query {\n  getByDate(created: Date!): Int\n}\n"""\n\n\n@given(\n    from_schema(\n        SCHEMA,\n        custom_scalars={\n            # Standard scalars work out of the box, for custom ones you need\n            # to pass custom strategies that generate proper AST nodes\n            "Date": st.dates().map(nodes.String)\n        },\n    )\n)\ndef test_graphql(query):\n    # Example:\n    #\n    #  { getByDate(created: "2000-01-01") }\n    #\n    ...\n```\n\nThe `hypothesis_graphql.nodes` module includes a few helpers to generate various node types:\n\n- `String` -> `graphql.StringValueNode`\n- `Float` -> `graphql.FloatValueNode`\n- `Int` -> `graphql.IntValueNode`\n- `Object` -> `graphql.ObjectValueNode`\n- `List` -> `graphql.ListValueNode`\n- `Boolean` -> `graphql.BooleanValueNode`\n- `Enum` -> `graphql.EnumValueNode`\n- `Null` -> `graphql.NullValueNode` (a constant, not a function)\n\nThey exist because classes like `graphql.StringValueNode` can\'t be directly used in `map` calls due to kwarg-only arguments.\n',
    'author': 'Dmitry Dygalo',
    'author_email': 'dadygalo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Stranger6667/hypothesis-graphql',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
