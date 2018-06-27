#!/usr/bin/env python

# Wrap code blocks in listing environment with caption

# By default, Pandoc adds captions to code blocks only
# when using the `--listings` option.
# However, the output of the `listings` is
# not as aesthetically pleasing as the one from Pandoc.
# I therefore add caption support to Pandoc without `--listings`.

# debugging
from __future__ import print_function
import sys
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

from pandocfilters import toJSONFilter, RawInline, Plain, CodeBlock

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
        (caption, _) = get_value(value[0][2], 'caption')
        
        block = CodeBlock(value[0], value[1])

        # we only need to add the caption, label is handled by Pandoc
        return \
            [ Plain([latex(r'\begin{listing}' + '\n' + \
                           r'\caption{' + caption + '}')]) \
            , block \
            , Plain([latex(r'\end{listing}')]) \
            ]

if __name__ == "__main__":
    toJSONFilter(listing)
