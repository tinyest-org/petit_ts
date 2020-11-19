from .ast_utils import get_extended_name, get_variable_name, set_extended_name
from typing import Any, Union, Literal, TypeVar


T = TypeVar('T')
# TODO: maybe setup a nice wrapper to be able to name any type


def Named(item: T) -> T:
    name = get_variable_name(with_raise=False)
    # if the same type has already been defined, then we get the previous object
    if get_extended_name(item) is not None:
        return item
    set_extended_name(item, name)
    return item
