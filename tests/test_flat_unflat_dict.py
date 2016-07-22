from snippets.flat_unflat_dict import flat, unflat

def test_flat():
    data = {
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
    expected = {
        'key2': ['one', 'two', 'three'],
        'key1_key12_key121': 'value121',
        'key1_key11_key111': 'value111'}

    expected_full = {
        'key1_key11_key111': 'value111',
        'key1_key12_key121': 'value121',
        'key2[0]': 'one',
        'key2[1]': 'two',
        'key2[2]': 'three',
    }


    data_list_dict = {
        "key1": [
            {
                "key11": {
                    "key111": "value111"
                }
            },
            {
                "key12": {
                    "key121": "value121"
                }
            }
        ]
    }

    expected_data_list = {
        'key1[0]_key11_key111': 'value111',
        'key1[1]_key12_key121': 'value121'
    }

    assert flat(data) == expected
    assert flat(data_list_dict, full=True) == expected_data_list
    assert flat(data, full=True) == expected_full


def test_unflat():
    expected = {
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

    data_full = {
        'key1_key11_key111': 'value111',
        'key1_key12_key121': 'value121',
        'key2[0]': 'one',
        'key2[1]': 'two',
        'key2[2]': 'three',
    }

    data = {
        'key2': ['one', 'two', 'three'],
        'key1_key12_key121': 'value121',
        'key1_key11_key111': 'value111'}


    assert unflat(data) == expected
    assert unflat(data_full) == expected

