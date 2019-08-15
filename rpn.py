import sys
from typing import List, Callable, Union, Optional, Tuple, get_type_hints

from stack import *

# Constants and typedefs
PROMPT = '> '
STREAM = sys.stdout
Op     = Callable[[int, int], int]
Cmd    = Callable[[Stack], Optional[int]]
Exp    = Union[int, Op, Cmd]

# Clean exit function
def quit(s: Stack) -> None:
    print(pop(s), file=sys.stdout)
    if STREAM != sys.stdout:
        STREAM.close()
    sys.exit()

# Pre-processing
def tokenize(entry: str) -> List[str]:
    return entry.split() if entry != '' else ['']

def is_valid(sym: str) -> bool:
    return (is_cmd(sym) or
            is_op(sym)  or
            all(ord(digit) > 47 and ord(digit) < 58 for digit in sym))

def is_cmd(token: str) -> bool:
    return token == 'q' or token == 'c' or token == ''

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
# (Since Callables are not comparable, I'm cheating by counting the type
# annotations in expressions that aren't ints. I would like to find a better
# solution that also appeases mypy)
def evaluate(s: Stack, e: Exp) -> Optional[int]:
    """ Evaluates RPN expressions """
    result = None
    if isinstance(e, int):
        result = push(s, e)
    elif len(get_type_hints(e).keys()) == 2:
        result = e(s)
    else:
        result = evaluate(s, e(pop(s), pop(s)))
    return result
        
# Main logic
def parser(stack: Stack, token: str) -> Optional[int]:
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
            print(str(parser(stack, t)), file=STREAM)
except EOFError:
    quit(stack)
