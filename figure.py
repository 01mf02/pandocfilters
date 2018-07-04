#!/usr/bin/env python

# debugging
from __future__ import print_function
import sys
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

from pandocfilters import toJSONFilter, RawInline
from pfcompat import get_value

def latex(x):
    return RawInline('latex', x)

def figure(key, value, format, meta):
    #eprint("Key: " + key)
    if key == 'Image':
        ident = value[0][0]
        kvs = value[0][2]
        caption = value[1]
        filename = value[2][0]
        
        if filename.endswith('.tex'):
            cmd = r'\input{' + filename + '}'
            width = get_value(kvs, 'width')[0]
            if width:
                fwidth = float(width.rstrip('%'))
                swidth = repr(fwidth / 100)
                cmd = r'\resizebox{' + swidth + r'\textwidth}{!}{' + cmd + '}'
        else:
            cmd = r'\includegraphics{' + filename + '}'

        return \
            [latex(r'\begin{figure}' + '\n' + \
                   cmd + '\n' + \
                   r'\caption{')] + \
            caption + \
            [latex('}' + '\n' + \
                   r'\label{' + ident + '}' + '\n' + \
                   r'\end{figure}')]

if __name__ == "__main__":
    toJSONFilter(figure)
