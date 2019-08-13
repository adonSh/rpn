import sys
from typing import List, Callable, Union, Optional

# Constants and typedefs
PROMPT = '> '
OUT    = sys.stdout
Stack  = List
Op     = Callable[[int, int], int]
Exp    = Union[int, Op]

# Stack operations
def empty(s: Stack[int]) -> None:
    return s.clear()

#TODO: make pop optional or at least evaluate
def pop(s: Stack[int]) -> int:
    return s.pop()

def peek(s: Stack[int]) -> Optional[int]:
    return s[len(s) - 1] if len(s) > 0 else None

def push(s: Stack[int], n: int) -> int:
    s.append(n)
    return n

# Pre-processing
def is_valid(sym: str) -> bool:
    return (sym == ''  or
            sym == 'q' or
            sym == 'c' or
            is_op(sym) or
            sym.isdigit()) # <- too pythonic

# Syntactic processing
def is_op(sym: str) -> bool:
    return (sym == '+' or 
            sym == '-' or
            sym == '*' or 
            sym == '/')

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

def read(sym: str) -> Exp:
    return op(sym) if is_op(sym) else int(sym)

# Semantic processing
def evaluate(s: Stack[int], e: Exp) -> int:
    return push(s, e) if isinstance(e, int) else evaluate(s, e(pop(s), pop(s)))

# Main logic
def interface(stack: Stack[int], entry: str) -> int:
    if not is_valid(entry):
        print('invalid input', file=OUT)
    elif entry == '': #TODO: mypy error here, check len better
        print(str(peek(stack), file=OUT) if len(stack) > 0 else 'stack is empty')
    elif entry == 'c':
        empty(stack)
    elif entry != 'q':
        if is_op(entry) and len(stack) < 2:
            print('too few arguments', file=OUT)
        else:
            print(str(evaluate(stack, read(entry))), file=OUT)
    else:
        if len(stack) > 0:
            print(pop(stack), file=sys.stdout)
        return 0
    return interface(stack, input(PROMPT))

# entry point
if len(sys.argv) > 1:
    if sys.argv[1] == '-q' or sys.argv[1] == '--quiet':
        PROMPT = ''
        OUT = open('/dev/null', 'w')
    else:
        print('invalid options')
        sys.exit(1)
stack: Stack[int] = []
sys.exit(interface(stack, input(PROMPT)))
