#!/usr/bin/env python

"""
Pandoc filter to convert links with a title to \index calls.
"""

# debugging
from __future__ import print_function
import sys
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

from pandocfilters import toJSONFilter, RawInline, Str, stringify

def latex(x):
    return RawInline('latex', x)

def linkindex(key, value, format, meta):
    #eprint("Key: " + key)
    if key == 'Link':
        #eprint(value)
        name = value[1]
        url = value[2][0]
        title = value[2][1]

        index = title if title else stringify(name) if url == '#' else []

        if index:
            if format == "latex":
                return name + [latex('\index{' + index + '}')]

if __name__ == "__main__":
    toJSONFilter(linkindex)
