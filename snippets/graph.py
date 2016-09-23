# -*- coding: utf-8 -*-
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
"""Generate a graph based on defined dict struct in a list
 and Jinja var management. The Graph is a dict.

Sometimes, I have to build a graph using a list of "resources" and
thoses resources could be dependent of each other.

To resolve dependency, we could analyse dependent variables and explicit
dependency with key requires.

The graph use a list as reference and as you know, the list is mutable
so we use generator to always generate the content (edges etc.).

To get a complete Graph course, code and more generate,
go on http://www.python-course.eu/graphs_python.php

This is not a class because I wan't to keep it more usable as possible.
You could create the class using static method to generate edges
and also the graph for example.

python:

- 2.6
- 2.7
- 3.4
- 3.5

requirements:

- Jinja2>=2.8 # for templating
- tox # for tests

author: Ahmet Demir <me@ahmet2mir.eu>

Example:

```python

>>> resources = [
        {
            'name': 'resource1',
            'inputs': {
                'key1': "{{ ignore.var1 }}"
            },
            'outputs': ['var1', 'var2'],
        },
        {
            'name': 'resource2',
            'inputs': {
                'key1': "{{ resource1.var1 }}",
                'key2': "{{ ignore.var1 }}",
            },
            'outputs': ['var1', 'var2'],
            'requires': ['resource3'],
        },
        {
            'name': 'resource3',
            'inputs': {
                'key1': "{{ resource1.var1 }}",
                'key2': "{{ resource2.var1 }}",
            },
            'outputs': ['var1', 'var2'],
        },
    ]
>>> print(list(generate_edges(resources))) # edges is a generator
[('resource1', 'resource1'),
 ('resource2', 'resource1'),
 ('resource3', 'resource1'),
 ('resource3', 'resource2')
]

```

Now we could generate the graph

```python
>>> print(generate_graph(generate_edges(resources)))
{'resource1': [],
 'resource3': ['resource1', 'resource2'],
 'resource2': ['resource1']}
```

If we update the list

```python
>>> resources.append({
        'name': 'resource4',
        'inputs': {
            'key1': "{{ resource1.var1 }}",
        },
        'outputs': ['var1', 'var2'],
    })
>>> print(list(generate_edges(resources)))
[('resource1', 'resource1'),
 ('resource2', 'resource1'),
 ('resource3', 'resource1'),
 ('resource3', 'resource2'),
 ('resource4', 'resource1') # new item
]
```

Regenerate the Graph

```python
{'resource1': [],
 'resource2': ['resource1'],
 'resource3': ['resource1', 'resource2'],
 'resource4': ['resource1']}
```

To identify isolated vertices (with no dependency)

```python
>>> edges = generate_edges(resources)
>>> print(list(find_isolated_vertices(edges)))
['resource1']
```

"""
from __future__ import (unicode_literals, absolute_import)
import json

# third libs
from jinja2 import (meta, Environment, FileSystemLoader)

# ignore some variable in resources
EDGES_IGNORES = ['ignore']

def generate_edges(resources):
    """ The connecting line between two resource is called an edge.
        Edges are directed from one vertex (resource) to another,
        the graph is called a directed graph. This function is
        used to construct the graph.

        Args:
            resources (list): resources list
    """
    for resource in resources:

        # convert to raw string
        raw = json.dumps(resource)
        env = Environment(loader=FileSystemLoader('templates'))
        vertex = resource['name']
        # direct dependency
        neighbors = []
        # jinja function find_undeclared_variables found not resolved vars
        for neighbour in meta.find_undeclared_variables(env.parse(raw)):
            if not neighbour in EDGES_IGNORES and neighbour != vertex\
                                            and not neighbour in neighbors:
                neighbors.append(neighbour)

        for neighbour in neighbors:
            yield (vertex, neighbour,)

        # isolated node
        if len(neighbors) == 0:
            yield (vertex, vertex,)


def find_isolated_vertices(edges):
    """ Returns a list of isolated vertices."""
    for edge in list(edges): # consume the generator
        if len(edge) == 2 and edge[0] == edge[1]:
            yield edge[0]


def generate_graph(edges):
    """ Generate a graph as dict using edges generator.

        Args:
            edges (generator): generator of edges.

        Returns:
            dict. the graph as
                {
                    "node": ["dependencies"],
                    ...
                }
    """
    graph = {}
    for edge in list(edges):
        if not edge[0] in graph:
            graph[edge[0]] = []

        if edge[1] and not edge[0] == edge[1]:
            graph[edge[0]].append(edge[1])
    return graph
