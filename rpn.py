import sys
from typing import List, Callable, Union, Optional

# Constants and typedefs
PROMPT = '> '
STREAM = sys.stdout
Op     = Callable[[int, int], int]
Exp    = Union[int, Op]
Stack  = List

# Stack operations
def empty(s: Stack[int]) -> None:
    s.clear()

def pop(s: Stack[int]) -> Optional[int]:
    return s.pop() if len(s) > 0 else None

def peek(s: Stack[int]) -> Optional[int]:
    return s[len(s) - 1] if len(s) > 0 else None

def push(s: Stack[int], n: int) -> int:
    s.append(n)
    return n

# Pre-processing
def is_valid(sym: str) -> bool:
    return (is_op(sym) or
            all(ord(digit) > 47 and ord(digit) < 58 for digit in sym))

def is_op(sym: str) -> bool:
    return (sym == '+' or 
            sym == '-' or
            sym == '*' or 
            sym == '/')

# Syntactic processing (must be given valid syntax)
def op(sym: str) -> Op:
    """ Generates genuine operators from syntactic forms """
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
    """ Generates RPN expressions """
    return op(sym) if is_op(sym) else int(sym)

# Semantic processing
def evaluate(s: Stack[int], e: Exp) -> Optional[int]:
    """ Evaluates RPN expressions """
    result = None
    if isinstance(e, int):
        result = push(s, e)
    else:
        x = pop(s)
        y = pop(s)
        if isinstance(x, int):
            if isinstance(y, int):
                result = evaluate(s, e(x, y))
            else:
                push(s, x)
    return result

# Main logic
def interface(stack: Stack[int], entry: str) -> int:
    """ Interface and preprocessor; responds to 'enter' (peek), 'q' (quit),
        and 'c' (clear) commands. Otherwise, evaluates RPN syntax """
    if entry == 'q':
        finalval = pop(stack)
        if isinstance(finalval, int):
            print(finalval, file=sys.stdout)
        if STREAM != sys.stdout:
            STREAM.close()
        return 0
    elif entry == 'c':
        empty(stack)
    elif entry == '':
        topval = peek(stack)
        print(str(topval) if isinstance(topval, int) else 'stack is empty',
              file=STREAM)
    elif is_valid(entry):
        result = evaluate(stack, read(entry))
        print(str(result) if isinstance(result, int) else 'too few arguments',
              file=STREAM)
    else:
        print('invalid input', file=STREAM)
    return interface(stack, input(PROMPT))

# entry point
if len(sys.argv) > 1:
    if sys.argv[1] == '-q' or sys.argv[1] == '--quiet':
        PROMPT = ''
        STREAM = open('/dev/null', 'w')
    else:
        print('invalid options')
        sys.exit(1)

try:
    sys.exit(interface([], input(PROMPT)))
except EOFError:
    print()
    sys.exit(0)
