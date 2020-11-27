from typing import TypeVar

from .ast_utils import get_extended_name, get_variable_name, set_extended_name

T = TypeVar('T')


def Named(item: T) -> T:
    name = get_variable_name(with_raise=False)
    # if the same type has already been defined, then we get the previous object
    if get_extended_name(item) is not None:
        return item
    set_extended_name(item, name)
    return item
