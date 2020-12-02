from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Literal, Optional, Tuple, Union, get_type_hints, get_origin, get_args

from petit_ts import ClassHandler, Named, TSTypeStore, patch_get_origin
# this makes us able, to use NamedUnion as Union for pydantic, without it we can't use 
# Named(Union[...])
patch_get_origin()

from pydantic import BaseModel

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


B = Named(Optional[Literal[1, 2, 'test_string']])

C = Named(Tuple[int, str])


F = Named(Union[str, int])
G = Named(Optional[Union[str, int, float]])


class L(BaseModel):
    p: str
    j: Optional[Union[str, int, None]]
    l: B
    # op: D
    # m: F
    # e: Union[F, G]


@dataclass
class Deb:
    a: int
    l: L
    dezo: Deb
    pp: D
    m: F
    e: Union[F, G]


D = Named(Optional[Tuple[C, Tuple[str, str]]])
A = Named(Optional[Union[int, str, Deb, B, C]])


store = TSTypeStore()
store.add_class_handler(BaseModelHandler)
store.get_repr(A)
print(store.get_repr(B))
print(store.get_full_repr(D))
print(store.get_all_not_inlined())

d = {
    'p':1, 
    'j':'',
    'l':1,
}

m = L(**d)
print(m)