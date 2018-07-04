# Functions added to pandocfilters since version 1.2.2

import codecs
import io
import json
import sys

from pandocfilters import walk, elt

def get_value(kv, key, value = None):
    """get value from the keyvalues (options)"""
    res = []
    for k, v in kv:
        if k == key:
            value = v
        else:
            res.append([k, v])
    return value, res

def toJSONFilters(actions):
    """Generate a JSON-to-JSON filter from stdin to stdout
    The filter:
    * reads a JSON-formatted pandoc document from stdin
    * transforms it by walking the tree and performing the actions
    * returns a new JSON-formatted pandoc document to stdout
    The argument `actions` is a list of functions of the form
    `action(key, value, format, meta)`, as described in more
    detail under `walk`.
    This function calls `applyJSONFilters`, with the `format`
    argument provided by the first command-line argument,
    if present.  (Pandoc sets this by default when calling
    filters.)
    """
    try:
        input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    except AttributeError:
        # Python 2 does not have sys.stdin.buffer.
        # REF: https://stackoverflow.com/questions/2467928/python-unicodeencode
        input_stream = codecs.getreader("utf-8")(sys.stdin)

    source = input_stream.read()
    if len(sys.argv) > 1:
        format = sys.argv[1]
    else:
        format = ""

    sys.stdout.write(applyJSONFilters(actions, source, format))

def applyJSONFilters(actions, source, format=""):
    """Walk through JSON structure and apply filters
    This:
    * reads a JSON-formatted pandoc document from a source string
    * transforms it by walking the tree and performing the actions
    * returns a new JSON-formatted pandoc document as a string
    The `actions` argument is a list of functions (see `walk`
    for a full description).
    The argument `source` is a string encoded JSON object.
    The argument `format` is a string describing the output format.
    Returns a the new JSON-formatted pandoc document.
    """

    doc = json.loads(source)

    if 'meta' in doc:
        meta = doc['meta']
    elif doc[0]:  # old API
        meta = doc[0]['unMeta']
    else:
        meta = {}
    altered = doc
    for action in actions:
        altered = walk(altered, action, format, meta)

    return json.dumps(altered)

# the version of pandocfilters defines Image to have only two arguments,
# whereas Pandoc gives it three
Image = elt('Image', 3)
