# -*- coding: utf-8 -*-
"""
Snippets module
"""
__all__ = []

import os
for item in os.listdir("snippets/"):
    if item[-2:] == "py":
        snippet = item.split(".")[0]
        if not snippet in __all__ and snippet[:1] != "_":
            __all__.append(snippet)
