from typing import Any, List, Tuple, Type

from petit_type_system import BasicHandler, ClassHandler
from petit_type_system.const import NoneType, undefined, null
from .handlers import (TSArrayHandler, TSDataclassHandler, TSEnumHandler,
                       TSLiteralHandler, TSMappingHandler, TSTupleHandler,
                       TSUnionHandler, TSStructHandler)
from petit_type_system.store import create_store_class


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
    TSEnumHandler,
    TSDataclassHandler,
]

ts_basic_handlers: List[Type[BasicHandler]] = [
    TSUnionHandler,
    TSLiteralHandler,
    TSArrayHandler,
    TSMappingHandler,
    TSTupleHandler,
]

TSTypeStore_ = create_store_class(
    ts_export_token,
    struct_handler=TSStructHandler,
    basic_handlers=ts_basic_handlers,
    class_handlers=ts_class_handlers,
    basic_types=ts_raw_default_types,
)


class TSTypeStore(TSTypeStore_):
    def __init__(self, export_all: bool = False, raise_on_error: bool = False, as_interface: bool = False):
        super().__init__(export_all=export_all, raise_on_error=raise_on_error)
        self.as_interface = as_interface
