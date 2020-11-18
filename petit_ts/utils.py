import inspect
import threading
from typing import (Any, Set, Tuple, TypeVar, Union, get_args, get_origin,
                    get_type_hints)

from .const import NoneType, pseudo_classes


class SafeCounter:
    def __init__(self, value: int = 0):
        self.value = value
        self.lock = threading.Lock()

    def increment(self, value: int = 1) -> int:
        with self.lock:
            self.value += value
        return self.value

    def decrement(self, value: int = 1) -> int:
        with self.lock:
            self.value -= value
        return self.value


def is_optional(cls: pseudo_classes) -> Tuple[bool, Tuple[Any]]:
    args = get_args(cls)
    return get_origin(cls) == Union and NoneType in args, args


def is_array(origin, args) -> bool:
    return origin == list and len(args) == 1


def is_mapping(origin, args) -> bool:
    return origin == dict and len(args) == 2


def __get_generic_params(cls: type, l: set) -> None:
    if inspect.isclass(cls):
        for type_ in get_type_hints(cls).values():
            if isinstance(type_, TypeVar):
                l.add(type_)
                continue
            args = get_args(type_)
            if len(args) > 0:
                __get_generic_params(type_, l)
    else:
        for arg in get_args(cls):
            if isinstance(arg, TypeVar):
                l.add(arg)
            args = get_args(arg)
            if len(args) > 0:
                __get_generic_params(arg, l)


def get_generic_params(cls: type) -> Set[TypeVar]:
    l = set()
    __get_generic_params(cls, l)
    return l


def is_generic(cls: type) -> Tuple[bool, Set[TypeVar]]:
    """Tells if a given class is generic
    """
    fields = get_generic_params(cls)
    return len(fields) > 0, fields
