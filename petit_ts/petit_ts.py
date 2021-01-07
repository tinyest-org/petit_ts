from __future__ import annotations

import inspect
from typing import (TYPE_CHECKING, Any, Dict, List, Optional, get_args,
                    get_origin)

from .const import pseudo_classes
from .exceptions import MissingHandler
from .utils import is_generic, is_optional

if TYPE_CHECKING:
    from .store import TypeStore # pragma: no cover 


class TypeStruct:
    """Internal object used to store the data in order to build, it's typescript representation
    """

    # TODO: use __slots__
    def __init__(
        self,
        value: pseudo_classes,  # TODO: nicer?
        store: TypeStore,
        exported: bool,
        *,
        default: bool = False,
        is_mapping_key: bool = False,
        raise_on_error: bool = False
    ):
        self.rendered: bool = False
        self.raise_on_error: bool = raise_on_error
        # should move to store.get_default_repr(value)
        self.__repr: str = f"any /* {value} */"

        if default:
            self.rendered = True
            self.__repr = value
        self.exported: bool = exported
        self.value: str = value
        self.rendering: bool = default
        self.store: TypeStore = store
        self.is_mapping_key = is_mapping_key
        self.name: Optional[str] = None

    def _make_inline(self, fields: Dict[str, Any]):
        # TODO: should move to ts-specific function
        s = []
        for key, type_ in fields.items():
            optional, args = is_optional(type_)
            if optional:
                if len(args) == 2:
                    self.store.add_type(type_)
                    s.append(
                        f'\t{key}?: {self.store.get_repr(args[0], is_mapping_key=True)}'
                    )
                # means that we have an Optional[Union[...]]
                else:
                    s.append(
                        f'\t{key}?: {self.store.get_repr(type_, is_mapping_key=True)}'
                    )
            else:
                s.append(
                    f'\t{key}: {self.store.get_repr(type_, is_mapping_key=True)}')
        self.__repr = '{ ' + ', '.join(s) + ' }'

    def _make_not_inline(self, name: str, fields: Dict[str, Any]):
        # TODO: should move to ts-specific function
        self.name = name
        is_generic_, names = is_generic(self.value)
        s: List[str] = []
        if is_generic_:
            s.append(
                f'type {self.name}<{", ".join(self.store.get_repr(n) for n in names)}> = {{'
            )
        else:
            s.append(f'type {self.name} = {{')
        for key, type_ in fields.items():
            optional, args = is_optional(type_)
            if optional:
                if len(args) == 2:
                    self.store.add_type(type_)
                    s.append(
                        f'\t{key}?: {self.store.get_repr(args[0], is_mapping_key=True)};'
                    )
                # means that we have an Optional[Union[...]]
                else:
                    s.append(
                        f'\t{key}?: {self.store.get_repr(type_, is_mapping_key=True)};'
                    )
            else:
                s.append(
                    f'\t{key}: {self.store.get_repr(type_, is_mapping_key=True)};')
        s.append('};')
        self.__repr = '\n'.join(s)

    def _render(self) -> None:
        """Here is the actual magic :) """
        if self.rendering:
            return
        self.rendering = True

        origin = get_origin(self.value)
        args = get_args(self.value)

        if inspect.isclass(self.value):
            for handler in self.store.class_handlers:
                if handler.should_handle(self.value, self.store, origin, args):
                    name, result = handler.build(
                        self.value, self.store, origin, args, self.is_mapping_key
                    )
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
                    self.rendered = True
                    self.rendering = False
                    return
            # TODO: better handle error
            if self.raise_on_error:
                print('HEY', self.value, inspect.isclass(self.value))
                raise MissingHandler(f'Type not Supported {self.value}')
        else:
            for handler in self.store.basic_handlers:
                if handler.should_handle(self.value, self.store, origin, args):
                    name, result = handler.build(
                        self.value, self.store, origin, args, self.is_mapping_key
                    )
                    self.__repr = result
                    if name is not None:
                        self.name = name
                    self.rendered = True
                    self.rendering = False
                    return

            # handle generic classes
            # other cases should have been handled before
            if len(args) > 0:
                self.__repr = f"{self.store.get_repr(origin)}<{', '.join(self.store.get_repr(i) for i in args)}>"
                self.rendered = True
                self.rendering = False
            else:
                self.rendering = False
                if self.raise_on_error:
                    raise MissingHandler(
                        f'No handler found for this type {self.value}'
                    )

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

    def get_full_repr(self, exported: bool = False) -> str:
        """Used to get the full body of not inlined type
        """
        if not self.rendered:
            self._render()
        if self.name != '':
            if self.exported or exported:
                return f'{self.store.export_token} {self.__repr}'
            return self.__repr
