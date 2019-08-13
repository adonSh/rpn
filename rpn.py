import sys
from typing import List, Callable, Union, Optional
from enum import Enum, auto

# Constants and typedefs
PROMPT = '> '
Stack = List
Op    = Callable[[int, int], int]
Exp   = Union[int, Op]

# Stack Operations
def empty(s: Stack[int]) -> None:
    return s.clear()

def pop(s: Stack[int]) -> int:
    return s.pop()

def peek(s: Stack[int]) -> Optional[int]:
    return s[-1] if len(s) > 0 else None

def push(s: Stack[int], n: int) -> int:
    s.append(n)
    return n

# Pre-processing functions
def is_op(sym: str) -> bool:
    return (sym == '+' or 
            sym == '-' or
            sym == '*' or 
            sym == '/')

def is_valid(sym: str) -> bool:
    return (sym == ''  or
            sym == 'q' or
            sym == 'c' or
            is_op(sym) or
            sym.isdigit()) # <- distastefully pythonic

def op(sym: str) -> Op:
    op: Op
    if sym == '+':
        op = lambda x, y: y + x
    elif sym == '-':
        op = lambda x, y: y - x
    elif sym == '*':
        op = lambda x, y: y * x
    elif sym == '/':
        op = lambda x, y: y // x
    return op

# Syntactic processing
def read(stk: Stack[int], sym: str) -> Exp:
    exp: Optional[Exp]
    if not is_valid(sym):
        print('invalid input')
        exp = read(stk, input(PROMPT))
    elif sym == 'q':
        sys.exit()
    elif sym == 'c':
        empty(stk)
        exp = read(stk, input(PROMPT))
    elif sym == '':
        exp = peek(stk)
        if not isinstance(exp, int):
            print('stack is empty')
            exp = read(stk, input(PROMPT))
    elif is_op(sym):
        if len(stk) > 1:
            exp = op(sym)
        else: 
            print('too few arguments')
            exp = read(stk, input(PROMPT))
    else:
        exp = int(sym)
    return exp

# Semantic Processing
def evaluate(s: Stack[int], e: Exp) -> int:
    return push(s, e if isinstance(e, int) else e(pop(s), pop(s)))

# Main logic
stack: Stack[int] = []

while True:
   print(str(evaluate(stack, read(stack, input(PROMPT)))))
