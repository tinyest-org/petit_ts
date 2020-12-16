from __future__ import annotations

from abc import ABC, abstractstaticmethod
from typing import Generic, TYPE_CHECKING, Any, Dict, List, Optional, Tuple, TypeVar, Union

if TYPE_CHECKING:
    from .petit_ts import TSTypeStore # pragma: no cover

T = TypeVar('T')


class BaseHandler(ABC, Generic[T]):

    @abstractstaticmethod
    def should_handle(cls: Any, store: TSTypeStore,
                      origin: Optional[type], args: List[Any]) -> bool: ...

    @abstractstaticmethod
    def build(cls: T, store: TSTypeStore, origin: Optional[type],
              args: List[Any], is_mapping_key:bool) -> Tuple[Optional[str], Union[str, Dict[str, Any]]]: ...


class BasicHandler(BaseHandler[T]):
    @abstractstaticmethod
    def build(cls: T, store: TSTypeStore, origin: Optional[type],
              args: List[Any], is_mapping_key:bool) -> Tuple[Optional[str], str]: ...


class ClassHandler(BaseHandler[T]):
    @abstractstaticmethod
    def is_mapping() -> bool: ...

    @abstractstaticmethod
    def build(cls: T, store: TSTypeStore, origin: Optional[type],
              args: List[Any], is_mapping_key:bool) -> Tuple[Optional[str], Union[str, Dict[str, Any]]]: ...
