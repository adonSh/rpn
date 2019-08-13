from typing import List, Callable, Union

Stack = List
Op    = Callable[[int, int], int]
Exp   = Union[int, Op]

def evaluate(s: Stack[int], e: Exp) -> int:
    val: int
    if isinstance(e, int):
        val = push(s, e)
    else:
        val = e(pop(s), pop(s))
    return val
