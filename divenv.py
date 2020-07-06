#!/usr/bin/env python

"""
Pandoc filter for replacing divs with LaTeX environments
"""

from pandocfilters import toJSONFilter, RawInline, Para

import re

def has_inlines(block):
    return ((block['t'] == "Para") | (block['t'] == "Plain"))

# Put inline lists `front` and `back` around `blocks`,
# avoiding the creation of new blocks if possible.
def encaps_blocks(front, blocks, back):
    if (has_inlines(blocks[0])):
        blocks[0]['c'][:0] = front
    else:
        blocks.insert(0, Para(front))

    if (has_inlines(blocks[-1])):
        blocks[-1]['c'].extend(back)
    else:
        blocks.append(Para(back))

def latex(x):
    return RawInline('latex', x)

def divenv(key, value, format, meta):
    if key == 'Div':
        [[id, classes, properties], content] = value

        for env in classes:
            label = [] if id == '' else [latex(r'\label{' + id + '}')]

            front = [latex(r'\begin{' + env + '}')] + label + [latex('\n')]
            back  = [latex('\n\\end{' + env + '}')]

            encaps_blocks(front, content, back)
            return content

if __name__ == '__main__':
    toJSONFilter(divenv)
