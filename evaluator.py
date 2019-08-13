from typing import List, Callable, Union

Stack = List
Op    = Callable[[int, int], int]
Exp   = Union[int, Op]

def evaluate(s: Stack[int], e: Exp) -> int:
    return push(s, e if isinstance(e, int) else e(pop(s), pop(s)))
