# coding: utf-8
import logging

import six
import pytest

from snippets.graph import find_isolated_vertices
from snippets.graph import generate_edges
from snippets.graph import generate_graph

RESOURCES = [
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


def test_edges():

    outputs = [
        ('resource1', 'resource1'),
        ('resource2', 'resource1'),
        ('resource3', 'resource1'),
        ('resource3', 'resource2')
    ]
    outputs_wrong = [
        ('fake', 'fake')
    ]
    edges = generate_edges(RESOURCES)
    result = []
    for edge in edges:
        result.append(edge)

    assert sorted(result) == sorted(outputs)
    assert sorted(result) != sorted(outputs_wrong)
    assert sorted(result) != []


def test_find_isolated_vertices():

    outputs = sorted(["resource1"])
    outputs_wrong = sorted(["resource1", "fake"])

    edges = generate_edges(RESOURCES)
    result = sorted(find_isolated_vertices(edges))

    assert result != None
    assert result != []
    assert result == outputs
    assert result != outputs_wrong

def test_graph():
    outputs = {'resource1': [],
               'resource3': ['resource1', 'resource2'],
               'resource2': ['resource1']}
    outputs_wrong = {'resource1': ["fake"]}

    edges = generate_edges(RESOURCES)
    result = generate_graph(edges)

    assert result != None
    assert result != []
    assert result == outputs
    assert result != outputs_wrong

