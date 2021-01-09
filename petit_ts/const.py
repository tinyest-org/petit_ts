from typing import Any, Final, List, Union, Tuple

INLINE_TOKEN: Final = "__inline__"

NoneType = type(None)


class undefined:
    """
    to use like undefined in typescript
    """
    ...


class null:
    """
    to use like null in typescript
    """
    ...


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



pseudo_classes = Union[dict, None, Any]

BASIC_TYPES = Union[int, str, float, bool, None]