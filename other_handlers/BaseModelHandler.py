from petit_ts.ts_store import TSTypeStore
from typing import List, Tuple, Optional, Dict, Any, get_type_hints
from petit_type_system import ClassHandler
from petit_ts import TSTypeStore
from pydantic import BaseModel


class BaseModelHandler(ClassHandler):
    @staticmethod
    def is_mapping() -> bool:
        return True

    @staticmethod
    def should_handle(cls: Any, store: TSTypeStore, origin: Any, args: List[Any]) -> bool:
        return issubclass(cls, BaseModel)

    @staticmethod
    def build(cls: BaseModel, store: TSTypeStore, origin, args) -> Tuple[Optional[str], Dict[str, Any]]:
        name = cls.__name__
        fields = get_type_hints(cls)
        return name, fields
