""" Integer stack for RPN calculator. Always contains at least one value (0)
"""
from typing import List

Stack = List[int]
INIT = 0

def new() -> Stack:
    return [INIT]

def empty(s: Stack) -> int:
    s.clear()
    return push(s, INIT)

def peek(s: Stack) -> int:
    return s[len(s) - 1] if len(s) > 0 else push(s, INIT)

def pop(s: Stack) -> int:
    return s.pop() if len(s) > 1 else peek(s)

def push(s: Stack, n: int) -> int:
    s.append(n)
    return n
