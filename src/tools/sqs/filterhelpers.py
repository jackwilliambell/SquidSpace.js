"""## SQS Filter Support API 

Shared code used by all SQS Filter Files Functions.
"""

import os
from filters.shellexec import filterFiles as shellexec_filter, __doc__ as shellexec_doc
from filters.merge import filterFiles as merge_filter, __doc__ as merge_doc
from filters.cleanbabylon import filterFiles as cleanbab_filter, __doc__ as cleanbab_doc


def getFilterModule(filterName):
    """Returns a tuple for the passed filter module name containing the filter files 
    function and the filter doc string. Returns 'None' if the filter could not be 
    located and/or loaded.
    
    TODO: Support dynamic imports from a 'filters' directory."""
    
    # Is it a 'built-in' filter?
    if filterName == "shellexec":
        return (shellexec_filter, shellexec_doc)
    elif filterName == "merge":
        return (merge_filter, merge_doc)
    elif filterName == "cleanbabylon":
        return (cleanbab_filter, cleanbab_doc)
    
    return (None, None)
