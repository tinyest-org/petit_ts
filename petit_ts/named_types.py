from typing import (Any, Callable, List, Optional, Tuple, TypeVar, Union,
                    get_args, get_origin)

from .ast_utils import get_variable_name

NAME_TOKEN = '__petit_name__'


class NamedUnion:
    ...


class NamedLiteral:
    ...


T = TypeVar('T')

# TODO: make a custom type that reflects the added functionnalities
ExtendedBasicTypeHint = Any


def get_extended_name(item: ExtendedBasicTypeHint) -> Optional[str]:
    if hasattr(item, NAME_TOKEN):
        return item.__dict__[NAME_TOKEN]
    else:
        return None


def set_extended_name(item: ExtendedBasicTypeHint, name: Optional[str], is_union: bool) -> None:
    i = item.copy_with(get_args(item))
    if name is not None:
        i.__dict__[NAME_TOKEN] = name
        if is_union:
            new_name = f'{name}NamedUnion'
            i.__origin__ = NamedUnion
            i.__repr__ = lambda: 'NamedUnion'
            i.__str__ = lambda: new_name
    return i


def Named(item: T) -> T:
    origin = get_origin(item)
    name = get_variable_name(with_raise=False)

    return set_extended_name(item, name, is_union=origin is Union)
