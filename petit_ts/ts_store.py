from typing import Any, List, Tuple, Type

from .base_handler import BasicHandler, ClassHandler
from .const import NoneType, undefined, null
from .handlers import (ArrayHandler, DataclassHandler, EnumHandler,
                       LiteralHandler, MappingHandler, TupleHandler,
                       UnionHandler)
from .store import TypeStore


def create_store_class(
    export_token: str,
    basic_types: List[Tuple[Any, str]],
    basic_handlers: List[Type[BasicHandler]],
    class_handlers: List[Type[ClassHandler]],
) -> Type[TypeStore]:

    class Store(TypeStore):
        _basic_handlers = basic_handlers
        _class_handlers = class_handlers
        _basic_types = basic_types
        _export_token = export_token

    return Store


ts_raw_default_types: List[Tuple[Any, str]] = [
    (bool, "boolean"),
    (None, "void"),
    (NoneType, "undefined"),

    (null, "null"),
    (undefined, "undefined"),

    (int, "number /*int*/"),
    (float, "number /*float*/"),

    (str, "string"),
    (dict, "object"),
    (list, "any[]"),

    (List[Any], "any[]"),
    (List, "any[]"),
    (List[int], "number[]"),
    (List[str], "string[]"),

    # any's
    (object, "any"),
    (Any, "any"),
]


# TS-specifics
ts_export_token = 'export'

ts_class_handlers: List[Type[ClassHandler]] = [
    EnumHandler,
    DataclassHandler,
]

ts_basic_handlers: List[Type[BasicHandler]] = [
    UnionHandler,
    LiteralHandler,
    ArrayHandler,
    MappingHandler,
    TupleHandler,
]

TSTypeStore = create_store_class(
    ts_export_token,
    basic_handlers=ts_basic_handlers,
    class_handlers=ts_class_handlers,
    basic_types=ts_raw_default_types,
)
