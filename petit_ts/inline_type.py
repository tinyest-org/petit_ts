from .utils import SafeCounter
from .const import INLINE_TOKEN
from dataclasses import make_dataclass

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