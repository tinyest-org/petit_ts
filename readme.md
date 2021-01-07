# Petit ts
![Codecov](https://img.shields.io/codecov/c/gh/plawn/petit_ts)
[![GitHub license](https://img.shields.io/github/license/Plawn/petit_ts)](https://github.com/Plawn/petit_ts/blob/main/LICENSE.TXT)

A Library to easly convert your python types to typescript types.

It's a part of the **petite_stack** (not released yet, as not mature enough).

### Example

```python
from petit_ts import TSTypeStore, Named

store = TSTypeStore()


class Jeb(Enum):
    A = 'R'


# if you want an union to be named and not inlined
UserType = Named(Literal['admin', 'user'])

TestUnion = Named(Union[str, int])

class CreateUserDto(BaseModel):
    username: str
    # will be inlined
    password: Union[str, Jeb]
    # won't be inlined
    role: UserType
    # won't be inlined
    jeb: TestUnion

store.add_type(CreateUserDto)

res = store.get_repr(CreateUserDto)
print(res)
# >>> "CreateUserDto"

# Here you notice that we have the name instead of the body, so that you can use it
# in another function easly

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

not_inlined = store.get_all_not_inlined(exported_all=True)
print(not_inlined)
# >>> "export type CreateUserDto  = {
# 	username: string;
# 	password: string | Jeb;
# 	role: UserType;
# 	jeb: TestUnion;
# };
# export enum Jeb {
# 	A = "R",
# };
# export type UserType = "admin" | "user";
# export type TestUnion = string | number /*int*/"


with open('res.ts', 'w') as f :
    # write what you need to the file
    final = f'export a = function (a: any): {store.get_repr(CreateUserDto)};'
    final += store.get_all_not_inlined()
    f.write(final)
```


### Supported types:

- None
- bool
- str
- int
- float
- Dict[K, V], Dict, dict
- List[T], List, list
- @dataclass, generic @dataclass
- Optional[T], Named(Optional[T])
- Union[A, B, ...], Named(Union[A, B, ...])
- Literal[values], Named(Literal[1, 2, '3']) with values = Union[int, str]
- Tuple[A, B, ...], Named(Tuple[A, B, ...])

### Add support for a custom type

Example for the BaseModel type:

```python

from typing import Tuple, Optional, Dict, Any, get_type_hints
from petit_ts import ClassHandler, TSTypeStore
from pydantic import BaseModel

store = TSTypeStore()

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


## Support for Named types:

if you need a type to be exported with it's definition name, you can use the `Named`function as such :

```python
P = Named(Union[str, int])
# will be exported to type P = string | number;
```

You can name any of :

- Optional
- Union
- Literal
- Tuple

If you have any problem, don't hesitate to open an issue on github !


## Support for type spoofing:


As you'll see with `pydantic.BaseModel`, NamedUnion is not supported by default because of the way the `Union`
is defined in the `typing` lib.

In order to support this, `petit_ts` provides the `patch_get_origin_for_Union`, it will make other libraries
believe `NamedUnion` is `Union`.
So you have to call `patch_get_origin_for_Union()` before importing pydantic.

## Next steps :

- Handle multiple type of collection
- Handle abstract types
- Choose between interface and type
- make petit-type-system -> petit-ts based on it with ts specific handlers
