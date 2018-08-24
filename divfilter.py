#!/usr/bin/env python

"""
Pandoc filter to filter out divs based on their class
"""

from pandocfilters import toJSONFilter

def divfilter(key, value, format, meta):
    if key == 'Div':

        [[id, classes, properties], content] = value

        for klass in classes:
            if klass in meta and meta[klass]['c'] == False:
                return []

if __name__ == '__main__':
    toJSONFilter(divfilter)
