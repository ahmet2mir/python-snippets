# force parent folder or you can use PYTHONPATH env variable.
import sys
sys.path.append("..")

from snippets.flat_unflat_dict import flat, unflat

if __name__ == '__main__':
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

    print(flat(data))
    print(flat(data, full=True))
    print(flat(data, full=True, lseparator=('{', '}')))
    print(flat(data, full=True, separator="."))

    flat_data = flat(data, full=True)
    print(unflat(flat_data))
