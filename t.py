from typing import Tuple
from petit_ts import TypeStore

def test_tuple():
    G = Tuple[Tuple[str, str]]
    store = TypeStore(export_all=False, raise_on_error=True)
    res = '[[string, string]]'
    # self.assertEqual(store.get_repr(G), res)
    assert store.get_repr(G) == res


if __name__ == '__main__':
    test_tuple()