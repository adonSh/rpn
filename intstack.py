""" Implementation of an immutable integer stack for RPN calculator.
    Always contains at least one value (0).
"""
from typing import List

Stack = List
INIT = 0

def new() -> Stack[int]:
    return [INIT]

def print(s: Stack[int]) -> Stack[int]:
    print(s)
    return s

def peek(s: Stack[int]) -> int:
    return s[len(s) - 1]

def pop(s: Stack[int]) -> Stack[int]:
    return s[:-1] if len(s) > 1 else s

def push(s: Stack[int], n: int) -> Stack[int]:
    return s + [n]
