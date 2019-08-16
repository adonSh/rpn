import sys
import inspect
from typing import List, Callable, Union, Optional, Tuple, get_type_hints, cast

from stack import *

# Constants and typedefs
PROMPT = '> '
STREAM = sys.stdout
Op     = Callable[[int, int], int]
Cmd    = Callable[[Stack[int]], int]
Exp    = Union[int, Op, Cmd]

# Clean exit function
def quit(s: Stack[int]) -> int:
    print(pop(s), file=sys.stdout)
    if STREAM != sys.stdout:
        STREAM.close()
    sys.exit()
    return 0 # never happens, exists solely so evaluate() always returns int

# Pre-processing
def tokenize(entry: str) -> List[str]:
    return entry.split() if entry != '' else ['']

def is_valid(sym: str) -> bool:
    return (is_cmd(sym) or
            is_op(sym)  or
            all(ord(digit) > 47 and ord(digit) < 58 for digit in sym))

def is_cmd(token: str) -> bool:
    return token == 'q' or token == 'c' or token == '' or token == 'p'

def is_op(token: str) -> bool:
    return token == '+' or token == '-' or token == '*' or token == '/'

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

def cmd(sym: str) -> Cmd:
    """ Generates command functions from syntactic forms """
    cmd: Cmd
    if sym == 'q':
        cmd = quit
    elif sym == 'c':
        cmd = empty
    elif sym == '':
        cmd = peek
    elif sym == 'p':
        cmd = lambda s: print(s)
    return cmd

def read(sym: str) -> Exp:
    """ Generates RPN expressions """
    exp: Exp
    if is_cmd(sym):
        exp = cmd(sym)
    elif is_op(sym):
        exp = op(sym)
    else:
        exp = int(sym)
    return exp

# Semantic processing
# TODO: Currently deducing type of expression from number of formal parameters
# and using cast to satisfy mypy. Feels sloppy.
def evaluate(s: Stack[int], e: Exp) -> int:
    """ Evaluates RPN expressions """
    result: int
    if isinstance(e, int):
        result = push(s, e)
    elif len(inspect.signature(e).parameters) == 1:
        result = cast(Cmd, e)(s)
    elif len(inspect.signature(e).parameters) == 2:
        result = evaluate(s, cast(Op, e)(pop(s), pop(s)))
    return result
        
# Main logic
def parser(stack: Stack[int], token: str) -> Optional[int]:
    """ Parser and preprocessor, sends valid RPN syntax to the evaluator """
    result = None
    if not is_valid(token):
        print('Syntax Error', file=STREAM)
    else:
        result = evaluate(stack, read(token))
    return result

# Entry point
if len(sys.argv) > 1:
    if sys.argv[1] == '-q' or sys.argv[1] == '--quiet':
        PROMPT = ''
        STREAM = open('/dev/null', 'w')
    else:
        print('invalid options', file=sys.stderr)
        sys.exit(1)

stack = new()
try:
    while True:
        for t in tokenize(input(PROMPT)):
            val = parser(stack, t)
            print(str(val) + '\n' if val != None else '', file=STREAM, end='')
except EOFError:
    print()
    quit(stack)
