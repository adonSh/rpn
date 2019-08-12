import sys
from typing import List, Callable, Tuple, Union, Optional
from enum import Enum, auto

Stack = List[int]
Op    = Callable[[int, int], int]
Exp   = Union[int, Op]

# Stack Operations
def empty(s: Stack) -> None:
    s.clear()

def pop(s: Stack) -> int:
    return s.pop()

def push(s: Stack, n: int) -> int:
    s.append(n)
    return n

# Interpreter functions
def is_op(sym: str) -> bool:
    return (sym == '+' or 
            sym == '-' or
            sym == '*' or 
            sym == '/')

def is_valid(sym: str) -> bool:
    return (sym == '\n' or
            sym == 'q'  or
            sym == 'c'  or
            is_op(sym)  or
            sym.isdigit())

def op(sym: str) -> Op:
    if sym == '+':
        return lambda x, y: y + x
    if sym == '-':
        return lambda x, y: y - x
    if sym == '*':
        return lambda x, y: y * x
#   if sym == '/':
    return lambda x, y: y // x

# Program logic
def read(sym: str) -> Tuple[Optional[Exp], Optional[str]]:
    if not is_valid(sym):
        return (None, 'invalid input')
    if sym == 'c':
        return (None, None)
    if sym == 'q':
        sys.exit()
    if is_op(sym):
        return (op(sym), None)
    return (int(sym), None)

def evaluate(s: Stack, e: Tuple[Optional[Exp], Optional[str]]) -> str:
    val = ''
    if isinstance(e[1], str):
        val = e[1]
    elif e[0] == None:
        empty(s)
    elif isinstance(e[0], int):
        val = str(push(s, e[0]))
    else:
        val = str(push(s, e[0](pop(s), pop(s)))) if len(s) > 1 else 'too few args'
    return val

# Main
stack: Stack = []

while True:
   print(evaluate(stack, read(input('> '))))
