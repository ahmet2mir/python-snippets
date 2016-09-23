# force parent folder or you can use PYTHONPATH env variable.
import sys
sys.path.append("..")

from snippets.graph import find_isolated_vertices
from snippets.graph import generate_edges
from snippets.graph import generate_graph

if __name__ == '__main__':

    resources = [
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


    print(list(generate_edges(resources)))
    print(generate_graph(generate_edges(resources)))

    resources.append({
        'name': 'resource4',
        'inputs': {
            'key1': "{{ resource1.var1 }}",
        },
        'outputs': ['var1', 'var2'],
    })

    print(list(generate_edges(resources)))
    print(generate_graph(generate_edges(resources)))

    edges = generate_edges(resources)
    print(list(find_isolated_vertices(edges)))
