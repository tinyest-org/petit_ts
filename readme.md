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

- bool
- str
- int
- float
- Dict[K, V]
- List[T]
- List, list
- Dict, dict