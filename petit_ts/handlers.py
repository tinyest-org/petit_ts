from dataclasses import is_dataclass
from enum import Enum
from typing import Any, Dict, Literal, Optional, Tuple, Union, get_type_hints, TYPE_CHECKING

from .ast_utils import get_extended_name
from .base_handler import BasicHandler, ClassHandler
from .const import INLINE_TOKEN

# if TYPE_CHECKING:
#     from .petit_ts import TSTypeStore


class UnionHandler(BasicHandler):
    @staticmethod
    def should_handle(cls, store, origin, args) -> bool:
        return origin is Union

    @staticmethod
    def build(cls: Union[Any], store, origin, args) -> Tuple[Optional[str], str]:
        # Union[Any] because Union is like Never
        if (name := get_extended_name(cls)) is None:
            return None, f' | '.join(store.get_repr(arg) for arg in args)
        else:
            return name, f'type {name} = '+' | '.join(store.get_repr(arg) for arg in args) + ';'


class LiteralHandler(BasicHandler):
    @staticmethod
    def should_handle(cls, store, origin, args) -> bool:
        return origin is Literal and len(args) > 0

    @staticmethod
    def build(cls: Literal, store, origin, args) -> Tuple[Optional[str], str]:
        name = get_extended_name(cls)
        is_inline = name is None
        s = []
        for arg in args:
            if isinstance(arg, int):
                s.append(f'{arg}')
            elif isinstance(arg, str):
                s.append(f'"{arg}"')
            else:
                # TODO: should add warning logger here
                print('error', arg)
        res = ' | '.join(s)
        if is_inline:
            return None, res
        else:
            return name, f'type {name} = {res};'


class EnumHandler(ClassHandler):
    @staticmethod
    def is_mapping() -> bool:
        return False

    @staticmethod
    def should_handle(cls: type, store, origin, args) -> bool:
        return issubclass(cls, Enum)

    @staticmethod
    def build(cls: Enum, store, origin, args) -> Tuple[Optional[str], str]:
        s = []
        name = cls.__name__
        for i in cls:
            if isinstance(i.value, str):
                s.append(f'\t{i.name} = "{i.value}",')
            elif isinstance(i.value, int):
                s.append(f'\t{i.name} = {i.value},')
            else:
                # TODO: handle error, invalid type
                pass
        res = f'enum {name} {{\n' + '\n'.join(s) + '\n};'
        return name, res


class DataclassHandler(ClassHandler):
    @staticmethod
    def is_mapping() -> bool:
        return True

    @staticmethod
    def should_handle(cls: type, store, origin, args) -> bool:
        return is_dataclass(cls)

    def is_inline(cls: type) -> bool:
        return cls.__name__.startswith(INLINE_TOKEN)

    @staticmethod
    def build(cls: type, store, origin, args) -> Tuple[Optional[str], Dict[str, Any]]:
        name = None if cls.__name__.startswith(INLINE_TOKEN) else cls.__name__
        fields = get_type_hints(cls)
        return name, fields
