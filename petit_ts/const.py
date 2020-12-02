from typing import Any, Final, List, Union

INLINE_TOKEN: Final = "__inline__"

NoneType = type(None)


class undefined:
    ...


class null:
    ...


DEFAULT_TYPES = {
    str(bool): "boolean",
    str(None): "void",
    str(NoneType): "undefined",
    str(null): "null",
    str(undefined): "undefined",
    str(Any): "any",
    str(int): "number /*int*/",
    str(float): "number /*float*/",
    str(str): "string",
    str(dict): "object",
    str(list): "any[]",
    str(List[Any]): "any[]",
    str(List): "any[]",
    str(List[int]): "number[]",
    str(List[str]): "string[]",
}

pseudo_classes = Union[dict, None, Any]
