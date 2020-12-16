import typing
from typing import Any, Callable, List, Tuple, Union

from .named_types import NamedUnion


def spoofer(spoofed: List[Tuple[Any, Any]]) -> Callable[[], None]:
    """Will return a function that will **replace** and **patch** the original function `get_origin` from
    the `typing` library.

    Warning, it could cause bug and side effects
    """
    def f() -> None:
        # this functions is copied/pasted from the typing library
        # it's also modified for spoofing types
        def get_origin(tp):
            """Get the unsubscripted version of a type.

            This supports generic types, Callable, Tuple, Union, Literal, Final and ClassVar.
            Return None for unsupported types. Examples::

                get_origin(Literal[42]) is Literal
                get_origin(int) is None
                get_origin(ClassVar[int]) is ClassVar
                get_origin(Generic) is Generic
                get_origin(Generic[T]) is Generic
                get_origin(Union[T, int]) is Union
                get_origin(List[Tuple[T, T]][int]) == list
            """
            if isinstance(tp, typing._GenericAlias):
                for fake, real in spoofed:
                    if tp.__origin__ is fake:
                        return real
                return tp.__origin__
            # this is copied and pasted from the real library so no need to test
            if tp is typing.Generic: # pragma: no cover 
                return typing.Generic # pragma: no cover
            return None

        typing.get_origin = get_origin
    return f


"""Will spooef NamedUnion as Union for other framewokr to not have errors
"""
patch_get_origin_for_Union = spoofer([
    (NamedUnion, Union),
])
