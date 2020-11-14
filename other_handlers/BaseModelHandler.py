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