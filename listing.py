#!/usr/bin/env python

# debugging
from __future__ import print_function
import sys
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

from pandocfilters import toJSONFilter, RawInline, Para
from subprocess import Popen, PIPE

def latex(x):
    return RawInline('latex', x)

def get_value(kv, key, value = None):
    """get value from the keyvalues (options)"""
    res = []
    for k, v in kv:
        if k == key:
            value = v
        else:
            res.append([k, v])
    return value, res

def listing(key, value, format, meta):
    #eprint("Key: " + key)
    if key == 'CodeBlock':
        ident = value[0][0]
        classes = value[0][1]
        kvs = value[0][2]
        code = value[1]
        (caption, _) = get_value(kvs, 'caption')
        
        dclasses = " ".join(map ((lambda x: "." + x), classes))
        stdin = '~~~ {' + dclasses + '}\n' + code + '\n~~~'

        p = Popen(['pandoc', '-t', 'latex'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate(stdin)

	lines = \
            [ r'\begin{listing}' \
            , stdout \
	    , r'\caption{' + caption + '}'
	    , r'\label{' + ident + '}' \
	    , r'\end{listing}'
	    ]
	return Para([latex('\n'.join(lines))])


if __name__ == "__main__":
    toJSONFilter(listing)
