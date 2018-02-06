def string(s):
    return [(s[0]['c'], s[1:])] if s and s[0]['t'] == 'Str'   else []
def space(s):
    return [(None     , s[1:])] if s and s[0]['t'] == 'Space' else []

def optional(f):
    def fun(s):
        result = f(s)
        if result == []:
            return [(None, s)]
        else:
            return result
    return fun

def satisfy(f, p):
    return (lambda s: ([(x, s1) for (x, s1) in f(s) if p(x)]))

def seq(f, g):
    return (lambda s: [((x, y), s2) for (x, s1) in f(s) for (y, s2) in g(s1)])

def seqr(f, g):
    return (lambda s: [(y, s1) for ((x, y), s1) in seq(f, g)(s)])
