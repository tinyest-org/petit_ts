# Petit ts


A Library to easly convert your python types to typescript types.

It's a part of the **petite_stack**.

### Example

```python
from petit_ts import T
store = TSTypeStore()


class Jeb(Enum):
    A = 'R'

UserType = NamedLiteral('admin', 'user')

TestUnion = NamedUnion(str, int)

class CreateUserDto(BaseModel):
    username: str
    password: Union[str, Jeb]
    role: UserType
    jeb: TestUnion

store.add_type(CreateUserDto)

res = store.get_repr(CreateUserDto)
print(res)
# >>> "CreateUserDto"

# here we need to do this in order, to get all the required deps into our ts file
not_inlined = store.get_all_not_inlined()
print(not_inlined)
# >>> "type CreateUserDto  = {
# 	username: string;
# 	password: string | Jeb;
# 	role: UserType;
# 	jeb: TestUnion;
# };
# export enum Jeb {
# 	A = "R",
# };
# type UserType = "admin" | "user";
# type TestUnion = string | number /*int*/"

with open('res.ts', 'w') as f :
    # write what you need to the file
    final = f'export a = function (a:any): {store.get_repr(CreateUserDto)};'
    final += store.get_all_not_inlined()
    f.write(final)

```


### Supported types:

- None
- bool
- str
- int
- float
- Dict[K, V]
- List[T]
- List, list
- Dict, dict
- @dataclass, generic @dataclass
- Optional[T]
- Union[A, B, ...], NamedUnion
- Literal[values], NamedLiteral with values = Union[int, str]

### Add support for a custom type

```python

from typing import Tuple, Optional, Dict, Any, get_type_hints
from petit_ts import ClassHandler
from pydantic import BaseModel


class BaseModelHandler(ClassHandler):
    @staticmethod
    def is_mapping() -> bool:
        return True

    @staticmethod
    def should_handle(cls, store, origin, args) -> bool:
        return issubclass(cls, BaseModel)

    @staticmethod
    def build(cls: BaseModel, store, origin, args) -> Tuple[Optional[str], Dict[str, Any]]:
        name = cls.__name__
        fields = get_type_hints(cls)
        return name, fields


store.add_class_handler(BaseModelHandler)
```

You have to implement for the `ClassHandler`:

- is_mapping
- should_handle
- build

If this is a mapping, you should return the fields, a `Dict[str, Any]` else you should return a string

For the BasicHandler :

- build
- should_handle
