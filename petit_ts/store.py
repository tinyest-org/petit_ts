from .petit_ts import TypeStruct
from typing import Any, Dict, Set, TypeVar, Type

from .base_handler import BaseHandler, BasicHandler, ClassHandler
from .const import BASIC_TYPES, pseudo_classes, raw_default_types
from .handlers import (ArrayHandler, DataclassHandler, EnumHandler,
                       LiteralHandler, MappingHandler, TupleHandler, UnionHandler)
from .utils import store_hash_function

DEFAULT_TYPES = {
    store_hash_function(cls): _repr for cls, _repr in raw_default_types
}


class TypeStore:
    # TODO: make interface and make different store for different languages
    """Required in order to link all the types between themselves
    Supports: 
    - `str`, `bool`, `int`, `float`, `Any`, `None` 
    - dict, list
    - Dict[K, V], L[T]
    - @dataclass and generic classes
    - `pydantic.BaseModel`


    (nested types are automaticcaly recurvely added so no need to add in the correct order, 
    generic classes are automaticcally added, if used once), 

    After adding all different wanted types :
    - store.render() and store.get_all_not_inlined()
    - Then you can use store.get_repr() for your classes 
    """
    export_token = 'export'

    def __init__(self, export_all: bool = False, raise_on_error: bool = False):
        self.export_all = export_all
        self.raise_on_error = raise_on_error
        self.types: Dict[str, TypeStruct] = {}
        
        # TODO: ts-specific
        # TODO: asset!
        # move to instances?
        self.class_handlers: Set[Type[ClassHandler]] = {
            EnumHandler,
            DataclassHandler,
        }
        # TODO: ts-specific
        # TODO: asset!
        # move to instances?
        self.basic_handlers: Set[Type[BasicHandler]] = {
            UnionHandler,
            LiteralHandler,
            ArrayHandler,
            MappingHandler,
            TupleHandler,
        }

        self.__init_default_type()

    def __init_default_type(self):
        self.types = {
            key: TypeStruct(value, self, False, default=True) for key, value in DEFAULT_TYPES.items()
        }

    def add_type(self, cls: pseudo_classes, exported: bool = False, is_mapping_key: bool = False) -> None:
        """Adds a type to the store in order to build it's representation in function of the others
        """
        if store_hash_function(cls) not in self.types:  # check if already built
            self.types[store_hash_function(cls)] = TypeStruct(
                cls,
                self,
                self.export_all or exported,
                is_mapping_key=is_mapping_key,
                raise_on_error=self.raise_on_error,
            )

    def render_types(self) -> None:
        """Use this to render actual store, not actually required, 
        because get_repr() will render if required
        """
        for type_ in list(self.types.values()):
            type_._render()

    def get_repr(self, cls: pseudo_classes, exported: bool = False, is_mapping_key: bool = False) -> str:
        """Returns the typescript representation of a given type
        """
        # handling generics
        if isinstance(cls, TypeVar):
            return cls.__name__

        if store_hash_function(cls) not in self.types:
            self.add_type(cls, exported, is_mapping_key)

        return self.types[store_hash_function(cls)].get_repr()

    def get_full_repr(self, cls: pseudo_classes, exported: bool = False) -> str:
        if isinstance(cls, TypeVar):
            return cls.__name__

        if store_hash_function(cls) not in self.types:
            self.add_type(cls)

        return self.types[store_hash_function(cls)].get_full_repr(exported=exported)

    def get_all_not_inlined(self, export_all: bool = False) -> str:
        """return all the function where a body has to be added to the file
        """
        # ensure rendered
        self.render_types()
        return '\n'.join(
            i.get_full_repr(exported=export_all) for i in self.types.values() if i.name is not None
        )

    def add_basic_handler(self, handler: Type[BasicHandler]) -> None:
        """Adds a `BasicHandler` to the store, in order to add support for a custom class

        if you want to add the support for datetime for example, it's here
        """
        self.basic_handlers.add(handler)

    def add_class_handler(self, handler: Type[ClassHandler]) -> None:
        """Adds a `ClassHandler` to the store, in order to add support for a custom class
        """
        self.class_handlers.add(handler)

    def add_basic_cast(self, type1: Any, type2: BASIC_TYPES) -> None:
        """For example if you want to cast datetime.datetime directly as str

        will only work for basic types | flat types
        """
        self.types[store_hash_function(
            type1)] = self.types[store_hash_function(type2)]
