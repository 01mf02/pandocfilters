from pfcompat import toJSONFilters
from figure import figure
from listing import listing
from linkref import linkref
from linkindex import linkindex
from defenv import defenvs
from divenv import divenv
from tabular import tabular

if __name__ == "__main__":
    toJSONFilters([linkindex, linkref, defenvs, divenv, tabular, listing, figure])
