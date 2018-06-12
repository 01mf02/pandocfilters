#!/usr/bin/env python

"""
Pandoc filter to convert links starting with "#" to \autoref calls.
"""

# debugging
from __future__ import print_function
import sys
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

from pandocfilters import toJSONFilter, RawInline, Str

def latex(x):
    return RawInline('latex', x)

def linkref(key, value, format, meta):
    #eprint("Key: " + key)
    if key == 'Link':
        #eprint(value)
        url = value[2][0]
        if url[0] == '#':
            labels = url[1:].split(";%20#")
            if format == "latex":
                return (latex('\\autoref{' + ",".join(labels) + '}'))
            elif format == "html" or format == "html5":
                # If no title given, set title to reference label
                if value[1] == []:
                    value[1] = [Str (label)]

if __name__ == "__main__":
    toJSONFilter(linkref)
