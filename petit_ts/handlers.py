from __future__ import annotations

from dataclasses import is_dataclass
from enum import Enum
from typing import (TYPE_CHECKING, Any, Dict, List, Literal, Optional, Tuple,
                    Union, get_type_hints)

from petit_type_system import BasicHandler, ClassHandler
from petit_type_system import StructHandler as BaseStructHandler
from petit_type_system.const import INLINE_TOKEN, NoneType
from petit_type_system.exceptions import InvalidTypeArgument
from petit_type_system.named_types import (NamedLiteral, NamedUnion,
                                           get_extended_name)
from petit_type_system.utils import is_generic, is_optional

if TYPE_CHECKING:
    from petit_type_system import TypeStore  # pragma: no cover


class UnionHandler(BasicHandler):
    @staticmethod
    def should_handle(cls, store, origin, args) -> bool:
        return origin in (NamedUnion, Union)

    @staticmethod
    def build(cls: Union[Any], store, origin, args, is_mapping_key: bool) -> Tuple[Optional[str], str]:
        # Union[Any] because Union is like Never
        if (name := get_extended_name(cls)) is None:
            if is_mapping_key:
                return None, f' | '.join(store.get_repr(arg) for arg in args if arg is not NoneType)
            else:
                return None, f' | '.join(store.get_repr(arg) for arg in args)
        else:
            return name, f'type {name} = '+' | '.join(store.get_repr(arg) for arg in args) + ';'


class LiteralHandler(BasicHandler):
    @staticmethod
    def should_handle(cls, store, origin, args) -> bool:
        return origin in (Literal, NamedLiteral)

    @staticmethod
    def build(cls: Literal, store, origin, args, is_mapping_key: bool) -> Tuple[Optional[str], str]:
        name = get_extended_name(cls)
        is_inline = name is None
        s = []
        for arg in args:
            if isinstance(arg, (int, float)):
                s.append(f'{arg}')
            elif isinstance(arg, str):
                s.append(f'"{arg}"')
            else:
                raise InvalidTypeArgument(
                    f'{arg} is neither a number instance, nor a string instance'
                )
        res = ' | '.join(s)
        if is_inline:
            return None, res
        else:
            return name, f'type {name} = {res};'


class EnumHandler(ClassHandler[Enum]):
    @staticmethod
    def is_mapping() -> bool:
        return False

    @staticmethod
    def should_handle(cls: type, store, origin, args) -> bool:
        return issubclass(cls, Enum)

    @staticmethod
    def build(cls: Enum, store, origin, args, is_mapping_key: bool) -> Tuple[Optional[str], str]:
        s = []
        name = cls.__name__
        for i in cls:
            if isinstance(i.value, str):
                s.append(f'\t{i.name} = "{i.value}",')
            elif isinstance(i.value, int):
                s.append(f'\t{i.name} = {i.value},')
            else:
                raise InvalidTypeArgument(
                    f'arg should be int, or str instance and got {i.value}'
                )
        res = f'enum {name} {{\n' + '\n'.join(s) + '\n};'
        return name, res


class DataclassHandler(ClassHandler):
    @staticmethod
    def is_mapping() -> bool:
        return True

    @staticmethod
    def should_handle(cls: type, store, origin, args) -> bool:
        return is_dataclass(cls)

    @staticmethod
    def build(cls: type, store, origin, args, is_mapping_key: bool) -> Tuple[Optional[str], Dict[str, Any]]:
        name = None if cls.__name__.startswith(INLINE_TOKEN) else cls.__name__
        fields = get_type_hints(cls)
        return name, fields


class TupleHandler(BasicHandler):
    @staticmethod
    def should_handle(cls: Any, store: TypeStore, origin: Optional[type], args: List[Any]) -> bool:
        return origin is tuple

    @staticmethod
    def build(cls: Any, store: TypeStore, origin: Optional[type], args: List[Any], is_mapping_key: bool) -> Tuple[Optional[str], Union[str, Dict[str, Any]]]:
        # Union[Any] because Union is like Never
        built = '[' + f', '.join(store.get_repr(arg)
                                 for arg in args if arg is not NoneType) + ']'
        if (name := get_extended_name(cls)) is None:
            return None, built
        else:
            return name, f'type {name} = {built}'


class ArrayHandler(BasicHandler):
    @staticmethod
    def should_handle(cls: Any, store: TypeStore, origin: Optional[type], args: List[Any]) -> bool:
        return origin == list and len(args) == 1

    @staticmethod
    def build(cls: List, store: TypeStore, origin: Optional[type], args: List[Any], is_mapping_key: bool) -> Tuple[Optional[str], str]:
        type_ = args[0]
        # can't have optional here
        built = f'({store.get_repr(type_)})[]'
        if (name := get_extended_name(cls)) is None:
            return None, built
        else:
            return name, f'type {name} = {built}'


class MappingHandler(BasicHandler):
    @staticmethod
    def should_handle(cls: Any, store: TypeStore, origin: Optional[type], args: List[Any]) -> bool:
        return origin == dict and len(args) == 2

    @staticmethod
    def build(cls: Any, store: TypeStore, origin: Optional[type], args: List[Any], is_mapping_key: bool) -> Tuple[Optional[str], str]:
        key_type, value_type = args
        # can't have optional here
        built = f'{{ [key: {store.get_repr(key_type)}]: {store.get_repr(value_type)} }}'
        if (name := get_extended_name(cls)) is None:
            return name,  built
        else:
            return name, f'type {name} = {built}'


class StructHandler(BaseStructHandler):
    @staticmethod
    def make_inline_struct(cls: Any, fields: Dict[str, Any], store: TypeStore) -> str:
        s = []
        for key, type_ in fields.items():
            optional, args = is_optional(type_)
            if optional:
                if len(args) == 2:
                    store.add_type(type_)
                    s.append(
                        f'{key}?: {store.get_repr(args[0], is_mapping_key=True)}'
                    )
                # means that we have an Optional[Union[...]]
                else:
                    s.append(
                        f'{key}?: {store.get_repr(type_, is_mapping_key=True)}'
                    )
            else:
                s.append(
                    f'{key}: {store.get_repr(type_, is_mapping_key=True)}')
        return '{ ' + ', '.join(s) + ' }'

    @staticmethod
    def make_struct(cls: Any, name: str, fields: Dict[str, Any], store: TypeStore) -> str:
        is_generic_, names = is_generic(cls)
        s: List[str] = []
        if is_generic_:
            s.append(
                f'type {name}<{", ".join(store.get_repr(n) for n in names)}> = {{'
            )
        else:
            s.append(f'type {name} = {{')
        for key, type_ in fields.items():
            optional, args = is_optional(type_)
            if optional:
                if len(args) == 2:
                    store.add_type(type_)
                    s.append(
                        f'\t{key}?: {store.get_repr(args[0], is_mapping_key=True)};'
                    )
                # means that we have an Optional[Union[...]]
                else:
                    s.append(
                        f'\t{key}?: {store.get_repr(type_, is_mapping_key=True)};'
                    )
            else:
                s.append(
                    f'\t{key}: {store.get_repr(type_, is_mapping_key=True)};')
        s.append('};')
        return '\n'.join(s)
