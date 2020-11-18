from typing import Any, List, Union
from pydantic import BaseModel

INLINE_TOKEN = "__inline__"

NoneType = type(None)

DEFAULT_TYPES = {
    str(bool): "boolean",
    str(None): "void",
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

pseudo_classes = Union[dict, None, Any, BaseModel]
