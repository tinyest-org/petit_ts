from typing import Literal, Union
from petit_ts import TSTypeStore, Named
from dataclasses import dataclass

@dataclass
class Deb:
    a:int
# print(globals()['Deb'])
B = Named(Literal[1, 2, '3'])
A = Named(Union[int, str, Deb, B])



store = TSTypeStore()
print(store.get_repr(A))
print(store.get_all_not_inlined())