#!/usr/bin/env python

# Convert Pandoc tables to floating tabular instead of longtable

# Adapted by Michael Faerber from:
# * https://gist.github.com/rriemann/56017da044861f7dd459dc5ab2f25cb9
# * https://groups.google.com/d/msg/pandoc-discuss/RUC-tuu_qf0/h-H3RRVt1coJ

import pandocfilters as pf

def latex(s):
    return pf.RawBlock('latex', s)

def inlatex(s):
    return pf.RawInline('latex', s)

def tbl_caption(s):
    return pf.Para([inlatex(r'\caption{')] + s + [inlatex('}')])

def tbl_alignment(s, default):
    aligns = {
        "AlignDefault": default,
        "AlignLeft": 'l',
        "AlignCenter": 'c',
        "AlignRight": 'r',
    }
    return ''.join([aligns[e['t']] for e in s])

def tbl_headers(s, delimiter):
    result = s[0][0]['c'][:]
    for i in range(1, len(s)):
        result.append(inlatex(' & '))
        if len(s[i]) > 0:
            result.extend(s[i][0]['c'])
    result.append(inlatex(delimiter))
    return pf.Para(result)

def tbl_contents(s, delimiter):
    result = []
    for row in s:
        para = []
        for col in row:
            if len(col) > 0:
                para.extend(col[0]['c'])
            para.append(inlatex(' & '))
        result.extend(para)
        result[-1] = inlatex(delimiter + '\n')
    return pf.Para(result)

def do_filter(k, v, f, m):
    if k == "Table":
        has_caption = (len(v[0]   ) > 0)
        has_header  = (len(v[3][0]) > 0)
        return \
              ([ latex(r'\begin{table}')
               , tbl_caption(v[0])] if has_caption else []) \
            +  [ latex(r'\begin{tabular}{%s}' % tbl_alignment(v[1], 'l'))
               , latex(r'\toprule')] \
            + ([ tbl_headers(v[3], r'\tabularnewline')
               , latex(r'\midrule')] if has_header else []) \
            +  [ tbl_contents(v[4], r'\tabularnewline')
               , latex(r'\bottomrule')
               , latex(r'\end{tabular}')] \
            + ([ latex(r'\end{table}')] if has_caption else [])

if __name__ == "__main__":
    pf.toJSONFilter(do_filter)
