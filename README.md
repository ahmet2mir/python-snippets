
# Python Snippets

A collection of Python function I use daily with examples, lint and tests.

Examples are described in the snippet docstring (in the README too) and could be located in `main` folder.

Tests are done with [tox](http://tox.testrun.org/) using [pytest](http://pytest.org/latest/) and [coverage](https://github.com/pytest-dev/pytest-cov) plugins.

To run the tests:

    $ pip install virtualenv
    $ virtualenv .venv
    $ source .venv/bin/activate
    $ pip install -r requirements.txt
    $ tox
    $ tox -e lint

_**Snippets summary:**_

* [Flat unflat dict](#flat-unflat-dict): Create a flat dict and unflat it.Could be useful if you use a key/value storage. ([download](https://raw.githubusercontent.com/ahmet2mir/python-snippets/master/snippets/flat_unflat_dict.py))
* [Graph](#graph): Generate a graph based on defined dict struct in a list and Jinja var management. The Graph is a dict. ([download](https://raw.githubusercontent.com/ahmet2mir/python-snippets/master/snippets/graph.py))

## Flat unflat dict
([download](https://raw.githubusercontent.com/ahmet2mir/python-snippets/master/snippets/flat_unflat_dict.py))

Create a flat dict and unflat it.
Could be useful if you use a key/value storage.

Based on mythsmith comment on http://stackoverflow.com/a/6027615

python:

- 2.6
- 2.7
- 3.4
- 3.5

requirements:

- tox # for tests

author: Ahmet Demir <me@ahmet2mir.eu>

Example:

```python
>>> data = {
        "key1": {
            "key11": {
                "key111": "value111"
            },
            "key12": {
                "key121": "value121"
            }
        },
        "key2": ["one","two", "three"]
    }

>>> print(flat(data))
{'key2': ['one', 'two', 'three'],
 'key1_key12_key121': 'value121',
 'key1_key11_key111': 'value111'}
```

In this case the list is not flat beacause you probably
wan't to make another work like a join on it.

If you wan't a "real" flat, use the param `full`.
The key will be append with the item position number in bracket.

```python
>>> print(flat(data, full=True))
{'key1_key11_key111': 'value111',
 'key1_key12_key121': 'value121',
 'key2[1]': 'two',
 'key2[2]': 'three',
 'key2[0]': 'one'}
```

Of course the separator could be customized with `separator` param.
Example, if you prefer the dot

```python
>>> print(flat(data, full=True, separator="."))
{'key1.key11.key111': 'value111',
 'key1.key12.key121': 'value121',
 'key2[1]': 'two',
 'key2[2]': 'three',
 'key2[0]': 'one'}
```

You could also use different separator for the full flat
with param `lseparator`

```python
>>> print(flat(data, full=True, lseparator=('{', '}')))
{'key1_key11_key111': 'value111',
 'key1_key12_key121': 'value121',
 'key2{1}': 'two',
 'key2{0}': 'one',
 'key2{2}': 'three'}
```

And finally, unflat it:

```python
>>> flat_data = flat(data, full=True)
>>> print(unflat(flat_data))
{
    'key1': {
        'key11': {
            'key111': 'value111'
        },
        'key12': {
            'key121': 'value121'
        }
    },
    'key2': ['one', 'two', 'three']
}
```

## Graph
([download](https://raw.githubusercontent.com/ahmet2mir/python-snippets/master/snippets/graph.py))

Generate a graph based on defined dict struct in a list
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


## License

Licensed under the Apache License, Version 2.0 (the "License"); you may
not use this file except in compliance with the License. You may obtain
a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations
under the License.

---

The README was generated by `gen_readme.py` at 2016-09-23T14:36:30.350Z
