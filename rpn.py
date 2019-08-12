#TODO: floats, better logic
import sys
from typing import List, Callable, Optional
from enum import Enum, auto

Stack = List[int]

def empty(s: Stack) -> str:
    s.clear()
    return ''

def pop(s: Stack) -> int:
    return s.pop()

def push(s: Stack, n: int) -> int:
    s.append(n)
    return n

def is_op(sym: str) -> bool:
    return (sym == '+' or 
            sym == '-' or
            sym == '*' or 
            sym == '/' or

def is_valid(sym: str) -> bool:
    return (sym == 'q' or
            sym == 'c' or
            is_op(sym) or
            sym.isdigit())

def op(sym: str) -> Callable[[int, int], int]:
    if sym == '+':
        return lambda x, y: y + x
    if sym == '-':
        return lambda x, y: y - x
    if sym == '*':
        return lambda x, y: y * x
#   if sym == '/':
    return lambda x, y: y // x

def eval(s: Stack, op: Callable[[int, int], int]) -> int:
    return push(s, op(pop(s), pop(s)))
    
def loop(s: Stack, cur: str) -> str:
    if not is_valid(cur):
        return 'invalid input'
    if cur == 'q':
        sys.exit()
    if cur == 'c':
        return empty(s)
    if is_op(cur):
        return str(eval(s, op(cur))) if len(s) > 1 else 'too few args'
    return str(push(s, int(cur)))

# main
stack: Stack = []

while True:
    print(loop(stack, input('> ')))
