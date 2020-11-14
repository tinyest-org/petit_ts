from .ast_utils import get_extended_name, get_variable_name, set_extended_name
from typing import Any, Union, Literal

# TODO: maybe setup a nice wrapper to be able to name any type


def NamedLiteral(*args: Union[str, int]) -> Literal:
    """Creates  a classic typing.Literal but with an added name, to enable type declaration
    """
    # normal litteral but wrapped
    item = eval('Literal[{}]'.format(
        ", ".join(str(arg) if isinstance(arg, int) else f'"{arg}"' for arg in args))
    )
    # gets the name of the variable which will be assigned
    name = get_variable_name(with_raise=False)
    # if the same type has already been defined, then we get the previous object
    if get_extended_name(item) is not None:
        return item
    set_extended_name(item, name)
    return item


def NamedUnion(*args: type) -> Union[Any]:
    """Creates  a classic typing.Union but with an added name, to enable type declaration

    note: the typing on this function is broken
    """
    # normal litteral but wrapped
    item = eval('Union[{}]'.format(", ".join(arg.__name__ for arg in args)))
    # gets the name of the variable which will be assigned
    name = get_variable_name(with_raise=False)
    # if the same type has already been defined, then we get the previous object
    if get_extended_name(item) is not None:
        return item
    set_extended_name(item, name)
    return item
