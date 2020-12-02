from typing import Any, Tuple, TypeVar, Union, get_origin
import typing
from .ast_utils import get_extended_name, get_variable_name, set_extended_name

_SpecialForm = typing._SpecialForm


class MyForm(_SpecialForm, _root=True):
    def __getitem__(self, typeargs: Tuple[Any]) -> object:
        name = get_variable_name(with_raise=False)
        t = super().__getitem__(typeargs)
        set_extended_name(t, name)
        return t

    def __hash__(self) -> int:
        if self._doc in ('NamedUnion', 'NamedLiteral'):
            return hash((self._doc,))
        raise Exception('not supported')

    def __eq__(self, other):
        if not isinstance(other, _SpecialForm):
            return NotImplemented
        return self._doc == other._name


NamedUnion = MyForm('Union', doc="NamedUnion")
NamedLiteral = MyForm('Literal', doc="NamedLiteral")

T = TypeVar('T')


def Named(item: T) -> T:
    origin = get_origin(item)
    if origin is Union:
        item.__origin__ = NamedUnion
    name = get_variable_name(with_raise=False)
    # if the same type has already been defined, then we get the previous object
    if get_extended_name(item) is not None:
        return item
    set_extended_name(item, name)
    return item
