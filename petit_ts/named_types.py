from typing import Any, Callable, List, Tuple, TypeVar, Union, get_origin
import typing
from .ast_utils import get_extended_name, get_variable_name, set_extended_name




class NamedUnion: ...
class NamedLiteral: ...


T = TypeVar('T')


def Named(item: T) -> T:
    origin = get_origin(item)
    if origin is Union:
        item.__origin__ = NamedUnion
        item.__repr__ = lambda: 'NamedUnion'
    name = get_variable_name(with_raise=False)
    # if the same type has already been defined, then we get the previous object
    if get_extended_name(item) is not None:
        return item
    set_extended_name(item, name)
    return item


