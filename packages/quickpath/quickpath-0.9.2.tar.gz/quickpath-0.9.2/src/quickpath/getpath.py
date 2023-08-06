""" This module provides easy access to elements of collection/object structures

Contains two kind of functions: getpath* to retrieve a single element from a collection and
getlistpath* to retrieve a list of elements according to the specified path 


    Typical usage example:

    item = [{'id': 1}, {'id': 2}]
    first_id = getpath(item, 0, 'id') 
    first_id = getpaths(item, '0.id') 
    all_ids = getlistpath(item, All, 'id') 
    all_ids = getlistpaths(item, '*.id')
    The 'first_id' variable will be 1 (the value which is corresponding to the 'id' key in the first dict).
    The 'all_ids' variable will be [1, 2] (values which are corresponding to the 'id' key in dicts).

"""

from collections.abc import Sequence, Mapping
from numbers import Integral
from typing import Any, Sequence as SequenceType


class PathOpType:
    pass


class AllType(PathOpType):
    pass


All = AllType()


def getpath(item: Any, index_terms: SequenceType[Any], default: Any = None) -> Any:
    """Returns a single value from an object hierarchy

    getpath([{'id': 1}, {'id': 2}], (0, 'id')) returns 1 (the value corresponds to the 'id' key in the first dict).
    The first element is always the expression referencing to the object root, then comes the rest of the keys.
    Mapping, sequence and generic objects are supported: mappings can be accessed with any type of keys, sequence types require integer keys,
    objects can be parametrized with string keys of their data attributes. If any of the keys, indexes, attributes
    do not exists, the default value is returned.

    Args:
        item: Any object hierarchy.
        index_terms: Sequence of valid key values.
        defaut: Default value returned in case of missing keys/attributes.

    Returns:
        A single value referenced by the "index terms".

    """
    item_to_proc = item

    for index_term in index_terms:
        if isinstance(item_to_proc, Mapping):
            if index_term in item_to_proc:
                item_to_proc = item_to_proc[index_term]
            else:
                return default
        elif isinstance(item_to_proc, Sequence) and (
            isinstance(index_term, PathOpType) or isinstance(index_term, Integral)
        ):
            if len(item_to_proc) > index_term:
                item_to_proc = item_to_proc[index_term]
            else:
                return default
        elif isinstance(index_term, str):
            try:
                item_to_proc = item_to_proc.getattr(index_term)
            except AttributeError as ae:
                return default
    return item_to_proc


def getpaths(item: Any, index_term_s: str, sep: str = ".", default: Any = None) -> Any:
    """Returns a single value from an object hierarchy

    getpath([{'id': 1}, {'id': 2}], '0.id') returns 1 (the value corresponds to the 'id' key in the first dict).
    The first element is always the expression referencing to the object root, then comes a streing representation of the rest of the keys.
    Mapping, sequence and generic objects are supported: mappings can be accessed with string keys, sequence types require integer keys,
    objects can be parametrized with string keys of their data attributes. If any of the keys, indexes, attributes
    do not exists, the default value is returned.

    Args:
        item: Any object hierarchy.
        index_term_s: String representation of the keys separated by the separator string.
        sep: The separator string.
        defaut: Default value returned in case of missing keys/attributes.

    Returns:
        A single value referenced by the "index terms" string.
    """
    index_tokens = index_term_s.split(sep)
    index_terms = ((int(token) if token.isdigit() else token) for token in index_tokens)
    return getpath(item, index_terms, default=default)


def getlistpath(item: Any, index_terms: SequenceType[Any]) -> SequenceType[Any]:
    item_to_proc = [item]

    for index_term in index_terms:
        result = []
        for item in item_to_proc:
            if isinstance(item, Mapping):
                if index_term in item:
                    result.append(item[index_term])
            elif isinstance(item, Sequence) and (
                isinstance(index_term, PathOpType) or isinstance(index_term, Integral)
            ):
                if index_term == All:
                    for subitem in item:
                        result.append(subitem)
                else:
                    if len(item) > index_term:
                        result.append(item[index_term])
            else:
                if hasattr(item, index_term):
                    result.append(getattr(item, index_term))
        if len(result) > 0:
            item_to_proc = result
        else:
            return result
    return item_to_proc


def getlistpaths(
    item: Any, index_term_s: str, sep=".", all_symb="*"
) -> SequenceType[Any]:
    index_terms = []
    for term in index_term_s.split(sep):
        if term == all_symb:
            index_terms.append(All)
        elif term.isdigit():
            index_terms.append(int(term))
        else:
            index_terms.append(term)

    return getlistpath(item, index_terms)

