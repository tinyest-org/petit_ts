from petit_ts.ts_store import TSTypeStore
from typing import List, Tuple, Optional, Dict, Any, get_type_hints
from petit_type_system import ClassHandler
from petit_ts import TSTypeStore
from pydantic import BaseModel


class BaseModelHandler(ClassHandler):
    def is_mapping(self) -> bool:
        return True

    def should_handle(self, cls: Any, origin: Any, args: List[Any]) -> bool:
        return issubclass(cls, BaseModel)

    def build(self, cls: BaseModel, origin, args) -> Tuple[Optional[str], Dict[str, Any]]:
        name = cls.__name__
        fields = get_type_hints(cls)
        return name, fields
