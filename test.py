from __future__ import annotations
from dataclasses import dataclass
from petit_ts.named_types import NamedUnion, NamedLiteral
from typing import Any, Dict, Literal, Optional, Tuple, Union, get_type_hints


from pydantic import BaseModel

from petit_ts import ClassHandler, Named, TSTypeStore


class BaseModelHandler(ClassHandler):
    @staticmethod
    def is_mapping() -> bool:
        return True

    @staticmethod
    def should_handle(cls, store, origin, args) -> bool:
        return issubclass(cls, BaseModel)

    @staticmethod
    def build(cls: BaseModel, store, origin, args) -> Tuple[Optional[str], Dict[str, Any]]:
        name = cls.__name__
        fields = get_type_hints(cls)
        return name, fields


B = Named(Optional[Literal[1, 2, '3']])

C = Named(Tuple[int, str])
D = Named(Tuple[C, Tuple[str, str]])
class L(BaseModel):
    p: str
    j: Optional[Union[str, int, None]]
    l: A
    op: C


@dataclass
class Deb:
    a: int
    l: L

A = Named(Optional[Union[int, str, Deb, B, C]])


store = TSTypeStore()
store.add_class_handler(BaseModelHandler)
print(store.get_repr(A))
print(store.get_repr(B))
print(store.get_full_repr(D))
print(store.get_all_not_inlined())
