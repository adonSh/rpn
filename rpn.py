import sys
import inspect
from typing import List, Callable, Union, Optional, Tuple, get_type_hints, cast

from stack import * #TODO: don't want this long-term

# Constants and typedefs
PROMPT  = '> '
STREAM  = sys.stdout
Op      = Callable[[int, int], int]
Cmd     = Callable[[Stack[int]], int]
ExpAtom = Union[int, Op, Cmd]
Exp     = Union[ExpAtom, List[ExpAtom]]

# Pre-processing
def tokenize(entry: str) -> List[str]:
    return entry.split() if entry != '' else ['']

def is_valid(token: str) -> bool:
    return (is_cmd(token) or
            is_op(token)  or
            all(ord(digit) > 47 and ord(digit) < 58 for digit in token))

def is_cmd(token: str) -> bool:
    return token == 'q' or token == 'c' or token == ''#or token == 'p'

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
#   elif sym == 'p':
#       cmd = lambda s: print(s)
    return cmd

def read(sym: str) -> ExpAtom:
    """ Generates atomic RPN expressions """
    exp: ExpAtom
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
    elif isinstance(e, list):
        if len(e) == 0:
            result = peek(s)
        else:
            evaluate(s, e[0])
            result = evaluate(s, e[1:])
    elif len(inspect.signature(e).parameters) == 1:
        result = cast(Cmd, e)(s)
    elif len(inspect.signature(e).parameters) == 2:
        result = evaluate(s, cast(Op, e)(pop(s), pop(s)))
    return result
        
# Main logic
def quit(s: Stack[int]) -> int:
    print(pop(s), file=sys.stdout)
    if STREAM != sys.stdout:
        STREAM.close()
    sys.exit()
    return 0 # never happens, exists solely so evaluate() always returns int

def parse(stack: Stack[int], tokens: List[str]) -> Optional[int]:
    """ Parser and preprocessor, sends valid RPN syntax to the evaluator """
    result = None
    if not all(is_valid(t) for t in tokens):
        print('Syntax Error', file=STREAM)
    else:
        result = evaluate(stack, list(map(read, tokens)))
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
        val = parse(stack, tokenize(input(PROMPT)))
        print(str(val) + '\n' if val != None else '', file=STREAM, end='')
except EOFError:
    print('', file=STREAM)
    quit(stack)
