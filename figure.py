#!/usr/bin/env python

# debugging
from __future__ import print_function
import sys
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

from pandocfilters import toJSONFilter, RawInline
from pfcompat import get_value, Image

def latex(x):
    return RawInline('latex', x)

def figure(key, value, format, meta):
    #eprint("Key: " + key)
    if key == 'Image':
        ident = value[0][0]
        classes = value[0][1]
        caption = value[1]
        image = Image(value[0], value[1], value[2])

        external = 'tikzexternal' in classes
        span     = 'span'         in classes
        env = 'figure*' if span else 'figure'

        return \
            [ latex(r'\begin{' + env + '}\n') \
            , latex(r'\tikzexternalenable' + '\n' if external else '') \
            , image, latex('\n') \
            , latex(r'\tikzexternaldisable' + '\n' if external else '') \
            , latex(r'\caption{') \
            ] + caption + \
            [ latex('}' + '\n') \
            , latex(r'\label{' + ident + '}' + '\n') \
            , latex(r'\end{' + env + '}') \
	    ]

if __name__ == "__main__":
    toJSONFilter(figure)
