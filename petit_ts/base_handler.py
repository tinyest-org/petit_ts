from typing import Tuple, Optional, Union, Any, Dict


class BaseHandler:
    @staticmethod
    def should_handle(cls, store, origin, args) -> bool: ...

    @staticmethod
    def build(cls, store, origin, args) -> Tuple[Optional[str], str]: ...


class BasicHandler(BaseHandler): ...


class ClassHandler(BaseHandler):
    @staticmethod
    def is_mapping() -> bool: ...

    @staticmethod
    def is_inline(cls) -> bool:
        return False

    @staticmethod
    def build(cls, store, origin, args) -> Tuple[Optional[str], Union[str, Dict[str, Any]]]: ...
