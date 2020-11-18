from __future__ import annotations

import inspect
from dataclasses import is_dataclass, make_dataclass
from enum import Enum
from typing import (Any, Dict, List, Optional, Set, TypeVar, get_args,
                    get_origin)

from pydantic import BaseModel

from .base_handler import BasicHandler, ClassHandler
from .const import INLINE_TOKEN, DEFAULT_TYPES, pseudo_classes
from .handlers import (DataclassHandler, EnumHandler, LiteralHandler,
                       UnionHandler)
from .utils import SafeCounter, is_array, is_generic, is_mapping, is_optional

# should handle string type


# we use this to create different names for the inlined types
"""Be careful with this, it's a global for the library
"""
global_counter = SafeCounter()


def Type(**kwargs) -> type:
    """Creates a dataclass in order to make an inline type

    example: Type(username=str, password=str) -> 
    ```python
    @dataclass
    class XXX:
        username: str
        password: str
    ```

    It can be used like that :
    ```python
    def handle_input(data: Type(username=str, password=str)) -> Type(error=bool):
        return {'error':False}
    ```
    """
    name = f'{INLINE_TOKEN}{global_counter.increment()}'
    return make_dataclass(name, [(key, type_) for key, type_ in kwargs.items()])


class TSTypeStore:
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

    def __init__(self):
        self.types: Dict[str, TypeStruct] = {}
        # we put them here, because they are less standard than the other
        self.basic_handlers: Set[BasicHandler] = {
            UnionHandler,
            LiteralHandler,
        }
        self.class_handlers: Set[ClassHandler] = {
            EnumHandler,
            DataclassHandler,
        }
        self.__init_default_type()

    def __init_default_type(self):
        self.types = {
            key: TypeStruct(value, self) for key, value in DEFAULT_TYPES.items()
        }

    def add_type(self, cls: pseudo_classes) -> None:
        """Adds a type to the store in order to build it's representation in function of the others
        """
        if str(cls) in self.types:  # already built
            return
        elif inspect.isclass(cls) and not any((issubclass(cls, BaseModel), issubclass(cls, Enum), is_dataclass(cls))):
            print('invalid class', cls, type(cls))
        else:
            self.types[str(cls)] = TypeStruct(cls, self)

    def render_types(self) -> None:
        """Use this to render actual store, not actually required, 
        because get_repr() will render if required
        """
        for type_ in list(self.types.values()):
            type_._render()

    def get_repr(self, cls: pseudo_classes) -> str:
        """Returns the typescript representation of a given type
        """
        if isinstance(cls, TypeVar):
            return cls.__name__
        if str(cls) not in self.types:
            self.add_type(cls)
        return self.types[str(cls)].get_repr()

    def get_all_not_inlined(self) -> str:
        """return all the function where a body has to be added to the file
        """
        return '\n'.join(
            i.get_full_repr() for i in self.types.values() if i.name is not None
        )

    def add_basic_handler(self, handler: BasicHandler) -> None:
        """Adds a `BasicHandler` to the store, in order to add support for a custom class

        if you want to add the support for datetime for example, it's here
        """
        self.basic_handlers.add(handler)

    def add_class_handler(self, handler: ClassHandler) -> None:
        """Adds a `ClassHandler` to the store, in order to add support for a custom class
        """
        self.class_handlers.add(handler)

    def add_cast(self, type1, type2) -> None:
        """For example if you want to cast datetime.datetime directly as str

        will only work for basic types | flat types
        """
        self.types[str(type1)] = self.types[str(type2)]


class TypeStruct:
    """Internal object used to store the data in order to build, it's typescript representation
    """

    def __init__(self, value: pseudo_classes, store: TSTypeStore):
        self.rendered = False
        self.__repr = f"any /* {value} */"
        # should make is cleaner
        try:
            if isinstance(value, str):
                self.rendered = True
                self.__repr = value
        except:
            print('error', value)
        self.value = value
        self.store = store
        self.name: Optional[str] = None

    def _make_inline(self, fields: Dict[str, Any]):
        s = []
        for key, type_ in fields.items():
            optional, args = is_optional(type_)
            if optional:
                s.append(
                    f'\t{key}?: {self.store.get_repr(args[0])}'
                )
            else:
                s.append(f'\t{key}: {self.store.get_repr(type_)}')
        self.__repr = '{ ' + ', '.join(s) + ' }'

    def _make_not_inline(self, name: str, fields: Dict[str, Any]):
        self.name = name
        is_generic_, names = is_generic(self.value)
        s: List[str] = []
        if not is_generic_:
            s.append(f'type {self.name}  = {{')
        else:
            s.append(
                f'type {self.name}<{", ".join(self.store.get_repr(n) for n in names)}> = {{'
            )
        for key, type_ in fields.items():
            optional, args = is_optional(type_)
            if optional:
                if len(args) == 2:
                    s.append(
                        f'\t{key}?: {self.store.get_repr(args[0])};'
                    )
                else:
                    # TODO: should log
                    print('error')
            else:
                s.append(f'\t{key}: {self.store.get_repr(type_)};')
        s.append('};')
        self.__repr = '\n'.join(s)

    def _render(self) -> None:
        """Here is the actual magic :) """
        if self.rendered:
            return
        self.rendered = True

        origin = get_origin(self.value)
        args = get_args(self.value)

        if inspect.isclass(self.value):
            for handler in self.store.class_handlers:
                if handler.should_handle(self.value, self.store, origin, args):
                    name, result = handler.build(
                        self.value, self.store, origin, args)
                    if not handler.is_mapping():
                        self.__repr = result
                    else:
                        if name is None:
                            self._make_inline(result)
                        else:
                            self._make_not_inline(name, result)
                    # we have the check twice, because if you are not a
                    #  mapping, you can still not be inline
                    if name is not None:
                        self.name = name
                    break
        else:
            for handler in self.store.basic_handlers:
                if handler.should_handle(self.value, self.store, origin, args):
                    name, result = handler.build(
                        self.value, self.store, origin, args
                    )
                    self.__repr = result
                    if name is not None:
                        self.name = name
                    return

            if isinstance(self.value, dict):
                s = []
                for key, value in self.value.items():
                    # should check optional
                    s.append(f'{key}: {self.store.get_repr(value)}')
                self.__repr = '{ '+', '.join(s)+' }'

            elif is_array(origin, args):
                type_ = args[0]
                # can't have optional here
                self.__repr = f'{self.store.get_repr(type_)}[]'

            elif is_mapping(origin, args):
                key_type, value_type = args
                # can't have optional here
                self.__repr = f'{{ [key: {self.store.get_repr(key_type)}]: {self.store.get_repr(value_type)} }}'

            # handle generic classes
            elif len(args) > 0:
                self.__repr = f"{self.store.get_repr(origin)}<{', '.join(self.store.get_repr(i) for i in args)}>"

    def get_repr(self) -> str:
        """returns the default representation for the type

        - inlined type will return their body

        - not inlined type will return their name
        """
        if not self.rendered:
            self._render()
        if self.name is not None:
            return self.name
        return self.__repr

    def get_full_repr(self) -> str:
        """Used to get the full body of not inlined type
        """
        if self.name != '':
            return self.__repr
