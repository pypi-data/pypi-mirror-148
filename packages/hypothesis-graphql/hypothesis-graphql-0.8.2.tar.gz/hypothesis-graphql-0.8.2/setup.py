# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hypothesis_graphql', 'hypothesis_graphql._strategies']

package_data = \
{'': ['*']}

install_requires = \
['attrs>20.3.0', 'graphql-core>=3.1.0,<4.0.0', 'hypothesis>5.8.0']

setup_kwargs = {
    'name': 'hypothesis-graphql',
    'version': '0.8.2',
    'description': 'Hypothesis strategies for GraphQL schemas and queries',
    'long_description': 'hypothesis-graphql\n==================\n\n|Build| |Coverage| |Version| |Python versions| |Chat| |License|\n\nHypothesis strategies for GraphQL schemas, queries and data.\n\n**NOTE** This package is experimental, some features are not supported yet.\n\nUsage\n-----\n\nThere are a few strategies for different use cases.\n\n1. Schema generation - ``hypothesis_graphql.strategies.schemas()``\n2. Query - ``hypothesis_graphql.strategies.queries(schema)``.\n3. Mutation - ``hypothesis_graphql.strategies.mutations(schema)``.\n\nLets take this schema as an example:\n\n.. code::\n\n    type Book {\n      title: String\n      author: Author\n    }\n\n    type Author {\n      name: String\n      books: [Book]\n    }\n\n    type Query {\n      getBooks: [Book]\n      getAuthors: [Author]\n    }\n\n    type Mutation {\n      addBook(title: String!, author: String!): Book!\n      addAuthor(name: String!): Author!\n    }\n\nThen strategies might be used in this way:\n\n.. code:: python\n\n    from hypothesis import given\n    from hypothesis_graphql import strategies as gql_st\n\n    SCHEMA = "..."  # the one above\n\n\n    @given(gql_st.queries(SCHEMA))\n    def test_query(query):\n        ...\n        # This query might be generated:\n        #\n        # query {\n        #   getBooks {\n        #     title\n        #   }\n        # }\n\n\n    @given(gql_st.mutations(SCHEMA))\n    def test_mutation(mutation):\n        ...\n        # This mutation might be generated:\n        #\n        # mutation {\n        #   addBook(title: "H4Z\\u7869", author: "\\u00d2"){\n        #     title\n        #   }\n        # }\n\nCustomization\n-------------\n\nTo restrict the set of fields in generated operations use the ``fields`` argument:\n\n.. code:: python\n\n    @given(gql_st.queries(SCHEMA, fields=["getAuthors"]))\n    def test_query(query):\n        # Only `getAuthors` will be generated\n        ...\n\nIt is also possible to generate custom scalars. For example, ``Date``:\n\n.. code:: python\n\n    from hypothesis import strategies as st, given\n    from hypothesis_graphql import strategies as gql_st, nodes\n\n    SCHEMA = """\n    scalar Date\n\n    type Query {\n      getByDate(created: Date!): Int\n    }\n    """\n\n\n    @given(\n        gql_st.queries(\n            SCHEMA,\n            custom_scalars={\n                # Standard scalars work out of the box, for custom ones you need\n                # to pass custom strategies that generate proper AST nodes\n                "Date": st.dates().map(nodes.String)\n            },\n        )\n    )\n    def test_query(query):\n        # Example:\n        #\n        #  { getByDate(created: "2000-01-01") }\n        #\n        ...\n\nThe ``hypothesis_graphql.nodes`` module includes a few helpers to generate various node types:\n\n- ``String`` -> ``graphql.StringValueNode``\n- ``Float`` -> ``graphql.FloatValueNode``\n- ``Int`` -> ``graphql.IntValueNode``\n- ``Object`` -> ``graphql.ObjectValueNode``\n- ``List`` -> ``graphql.ListValueNode``\n- ``Boolean`` -> ``graphql.BooleanValueNode``\n- ``Enum`` -> ``graphql.EnumValueNode``\n- ``Null`` -> ``graphql.NullValueNode`` (a constant, not a function)\n\nThey exist because classes like ``graphql.StringValueNode`` can\'t be directly used in ``map`` calls due to kwarg-only arguments.\n\n.. |Build| image:: https://github.com/Stranger6667/hypothesis-graphql/workflows/build/badge.svg\n   :target: https://github.com/Stranger6667/hypothesis-graphql/actions\n.. |Coverage| image:: https://codecov.io/gh/Stranger6667/hypothesis-graphql/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/Stranger6667/hypothesis-graphql/branch/master\n   :alt: codecov.io status for master branch\n.. |Version| image:: https://img.shields.io/pypi/v/hypothesis-graphql.svg\n   :target: https://pypi.org/project/hypothesis-graphql/\n.. |Python versions| image:: https://img.shields.io/pypi/pyversions/hypothesis-graphql.svg\n   :target: https://pypi.org/project/hypothesis-graphql/\n.. |Chat| image:: https://img.shields.io/gitter/room/Stranger6667/hypothesis-graphql.svg\n   :target: https://gitter.im/Stranger6667/hypothesis-graphql\n   :alt: Gitter\n.. |License| image:: https://img.shields.io/pypi/l/hypothesis-graphql.svg\n   :target: https://opensource.org/licenses/MIT\n',
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
