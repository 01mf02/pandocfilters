#!/usr/bin/env python

"""
Pandoc filter to convert definitions to LaTeX environments.
"""

# debugging
from __future__ import print_function
import sys
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

from pandocfilters import toJSONFilter, Para, RawInline, DefinitionList, stringify

import string
import parse


def latex(x):
    return RawInline('latex', x)

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

def parse_name(inlines):
    if inlines[ 0]['t'] == 'Str' and inlines[ 0]['c'][ 0] == '(' and \
       inlines[-1]['t'] == 'Str' and inlines[-1]['c'][-1] == ')':
        result = inlines
        result[ 0]['c'] = result[ 0]['c'][1:]
        result[-1]['c'] = result[-1]['c'][:-1]
        return [(result, [])]
    return []


def defenv(definition, contents):
    '''
    eprint("Def:")
    eprint(definition)
    eprint("Cnt:")
    eprint(contents)
    '''

    parse_typ = parse.string
    parse_label = parse.satisfy(parse.string, lambda x: x[0] != '(')
    parse_olabel = parse.optional(parse.seqr(parse.space, parse_label))
    parse_oname  = parse.optional(parse.seqr(parse.space, parse_name ))
    parse_def = parse.seq(parse_typ, parse.seq(parse_olabel, parse_oname))

    [((typ, (label, name)), rem)] = parse_def(definition)
    """
    eprint(parse_def(definition))
    eprint("Typ: " + typ)
    eprint("Label:")
    eprint(label)
    eprint("Name:")
    eprint(name)
    """

    typ = typ.lower()
    name  = [] if name  is None else [latex("[")] + name + [latex("]")]
    label = [] if label is None else [latex('\\label{' + label + '}')]

    front = [latex('\\begin{' + typ + '}')] + name + label
    back  = [latex('\\end{'   + typ + '}')]

    encaps_blocks(front, contents, back)
    return contents

def defenvs(key, value, format, meta):
    #eprint("Key: " + key)
    if key == 'DefinitionList':
        return ([x for [definition, [contents]] in value
                   for x in defenv(definition, contents)])

if __name__ == "__main__":
    toJSONFilter(defenvs)
