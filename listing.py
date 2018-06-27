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
from pfcompat import get_value

def latex(x):
    return RawInline('latex', x)

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
