from __future__ import annotations

from abc import ABC, abstractstaticmethod
from typing import Generic, TYPE_CHECKING, Any, Dict, List, Optional, Tuple, TypeVar, Union

if TYPE_CHECKING:
    from .store import TypeStore  # pragma: no cover

T = TypeVar('T')


class BaseHandler(ABC, Generic[T]):

    @abstractstaticmethod
    def should_handle(cls: Any, store: TypeStore,
                      origin: Optional[type], args: List[Any]) -> bool:
        ...

    @abstractstaticmethod
    def build(cls: T, store: TypeStore, origin: Optional[type],
              args: List[Any], is_mapping_key: bool) -> Tuple[Optional[str], Union[str, Dict[str, Any]]]:
        ...


class BasicHandler(BaseHandler[T]):
    @abstractstaticmethod
    def build(cls: T, store: TypeStore, origin: Optional[type],
              args: List[Any], is_mapping_key: bool) -> Tuple[Optional[str], str]:
        ...


class ClassHandler(BaseHandler[T]):
    @abstractstaticmethod
    def is_mapping() -> bool:
        ...

    @abstractstaticmethod
    def build(cls: T, store: TypeStore, origin: Optional[type],
              args: List[Any], is_mapping_key: bool) -> Tuple[Optional[str], Union[str, Dict[str, Any]]]:
        ...


class StructHandler(ABC):
    @abstractstaticmethod
    def make_inline_struct(cls: Any, fields: Dict[str, Any], store: TypeStore) -> str:
        ...

    @abstractstaticmethod
    def make_struct(cls: Any, name:str, fields: Dict[str, Any], store: TypeStore) -> str:
        pass
