import sys
from typing import List, Callable, Union, Optional, Tuple

# Constants and typedefs
PROMPT = '> '
STREAM = sys.stdout
Stack  = List
Op     = Callable[[int, int], int]
Cmd    = Callable[[Stack[int]], int]
Exp    = Tuple[Union[int, Op, Cmd],str]

def quit(s: Stack[int]) -> None:
    finalval = pop(s)
    if isinstance(finalval, int):
        print(finalval, file=sys.stdout)
    if STREAM != sys.stdout:
        STREAM.close()
    sys.exit()

# Stack operations
def empty(s: Stack[int]) -> int:
    s.clear()
    return push(s, 0)

def peek(s: Stack[int]) -> Optional[int]:
    return s[len(s) - 1] if len(s) > 0 else None

def pop(s: Stack[int]) -> Optional[int]:
    return s.pop() if len(s) > 0 else None

def push(s: Stack[int], n: int) -> int:
    s.append(n)
    return n

# Pre-processing
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
#   return list(map(lambda sym: (cmd(sym), 'cmd') if is_cmd(sym) else (op(sym), 'op') if is_op(sym) else (int(sym), 'num'), syntax))
    exp: Exp
    if is_cmd(sym):
        exp = (cmd(sym), 'cmd')
    elif is_op(sym):
        exp = (op(sym), 'op')
    else:
        exp = (int(sym), 'num')
    return exp

# Semantic processing
def evaluate(s: Stack[int], e: Exp) -> int:
    """ Evaluates RPN expressions """
    result: int
    if e[1] == 'cmd':
        result = e[0](s)
    elif e[1] == 'num':
        result = push(s, e[0])
    elif e[1] == 'op':
        x = pop(s)
        y = pop(s)
        if isinstance(x, int):
            if isinstance(y, int):
                result = evaluate(s, (e[0](x, y), 'num'))
            else:
                result = push(s, x)
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

stack = [0]
try:
    while True:
        print(str(parser(stack, input(PROMPT))))
except EOFError:
    print()
    sys.exit(0)
