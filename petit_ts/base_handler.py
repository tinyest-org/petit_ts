from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Tuple, Optional, Union, Any, Dict, TYPE_CHECKING, List

if TYPE_CHECKING:
    from .petit_ts import TSTypeStore


class BaseHandler(ABC):
    
    @staticmethod
    @abstractmethod
    def should_handle(cls: Any, store: TSTypeStore,
                      origin: Optional[type], args: List[Any]) -> bool: ...

    
    @staticmethod
    @abstractmethod
    def build(cls: Any, store: TSTypeStore, origin: Optional[type],
              args: List[Any]) -> Tuple[Optional[str], Union[str, Dict[str, Any]]]: ...


class BasicHandler(BaseHandler):
    @staticmethod
    @abstractmethod
    def build(cls: Any, store: TSTypeStore, origin: Optional[type],
              args: List[Any]) -> Tuple[Optional[str], str]: ...


class ClassHandler(BaseHandler):
    @staticmethod
    @abstractmethod
    def is_mapping() -> bool: ...

    @staticmethod
    def is_inline(cls: type) -> bool:
        return False

    @staticmethod
    @abstractmethod
    def build(cls, store: TSTypeStore, origin: Optional[type],
              args: List[Any]) -> Tuple[Optional[str], Union[str, Dict[str, Any]]]: ...
