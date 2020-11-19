from typing import Literal, Union
from petit_ts import TSTypeStore, Named
from dataclasses import dataclass

from typing import Tuple, Optional, Dict, Any, get_type_hints
from petit_ts import ClassHandler
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


class L(BaseModel):
    p: str


@dataclass
class Deb:
    a: int
    l: L


# print(globals()['Deb'])
B = Named(Literal[1, 2, '3'])
A = Named(Union[int, str, Deb, B])


store = TSTypeStore()
store.add_class_handler(BaseModelHandler)
print(store.get_repr(A))
print(store.get_all_not_inlined())
