from abc import ABC, abstractmethod
from typing import Tuple, Optional, Union, Any, Dict, TYPE_CHECKING, List

if TYPE_CHECKING:
    from .petit_ts import TSTypeStore


class BaseHandler(ABC):
    @abstractmethod
    @staticmethod
    def should_handle(cls: Any, store: TSTypeStore,
                      origin: Optional[type], args: List[Any]) -> bool: ...

    @abstractmethod
    @staticmethod
    def build(cls: Any, store: TSTypeStore, origin: Optional[type],
              args: List[Any]) -> Tuple[Optional[str], Union[str, Dict[str, Any]]]: ...


class BasicHandler(BaseHandler):
    @abstractmethod
    @staticmethod
    def build(cls: Any, store: TSTypeStore, origin: Optional[type],
              args: List[Any]) -> Tuple[Optional[str], str]: ...


class ClassHandler(BaseHandler):
    @abstractmethod
    @staticmethod
    def is_mapping() -> bool: ...

    @staticmethod
    def is_inline(cls: type) -> bool:
        return False

    @abstractmethod
    @staticmethod
    def build(cls, store: TSTypeStore, origin: Optional[type],
              args: List[Any]) -> Tuple[Optional[str], Union[str, Dict[str, Any]]]: ...
