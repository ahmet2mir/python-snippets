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
"""Create a flat dict and unflat it.
Could be useful if you use a key/value storage.

Based on mythsmith comment on http://stackoverflow.com/a/6027615

python:

- 2.6
- 2.7
- 3.4
- 3.5

requirements:

- tox

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

"""
import re
import collections

def unflat(data, separator="_", lseparator=('[', ']')):
    """
    Unflat the dict

    Args:
        data (dict): the dict to unflat. Must be a key/value dict.
        separator (:obj:`str`, optional): key separator.

    Returns:
        dict: Unflatted dict
    """
    unflat_dict = {}
    for k in sorted(data.keys()):
        context = unflat_dict
        for sub_key in k.split(separator)[:-1]:
            if sub_key not in context:
                context[sub_key] = {}
            context = context[sub_key]

        key = k.split(separator)[-1]

        regex = r'(\w*)\{0}(\d)\{1}'.format(lseparator[0], lseparator[1])
        match = re.match(regex, key)
        if match:
            lkey = match.group(1)
            lpos = int(match.group(2))

            if not lkey in context:
                context[lkey] = []
            context[lkey].insert(lpos, data[k])
        else:
            context[key] = data[k]
    return unflat_dict


def flat(data, prefix=None, separator='_', full=False,\
         lseparator=('[', ']')):
    """
    Flat the dict

    Args:
        data (dict): the dict to flat. Must be a key/value dict.
        separator (:obj:`str`, optional): key separator, defaults is _
        prefix (:obj:`str`, optional): prefix key with a string value,
            defaults is None
        lseparatort (:obj:`tuple`, optional): tuple of bracket for
            full flat, defaults is ('[', ']').

    Returns:
        dict: flatted dict
    """
    items = []
    for k in sorted(data.keys()):
        new_key = k
        if prefix:
            new_key = prefix + separator + k
        if isinstance(data[k], dict):
            items.extend(flat(data[k], new_key, separator, full).items())
        else:
            if full:
                if isinstance(data[k], list):
                    for i, value in enumerate(data[k]):
                        pkey = new_key + lseparator[0] + str(i)\
                               + lseparator[1]
                        if isinstance(value, collections.MutableMapping):
                            flated = flat(value, pkey, separator, full)
                            items.extend(flated.items())
                        else:
                            items.append((pkey, value))
                else:
                    items.append((new_key, data[k]))
            else:
                items.append((new_key, data[k]))

    return dict(items)
