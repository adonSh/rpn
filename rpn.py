import sys
from typing import List, Callable, Union, Optional, Tuple, cast

import stack

# Constants and typedefs
PROMPT  = '> '
STREAM  = sys.stdout
Stack   = stack.Stack
Op      = Callable[[Stack[int]], int]
ExpAtom = Union[int, Op]
Exp     = Union[ExpAtom, List[ExpAtom]]

# Pre-processing
def tokenize(entry: str) -> List[str]:
    return entry.split()

def is_valid(token: str) -> bool:
    return (is_op(token)  or
            all(ord(digit) > 47 and ord(digit) < 58 for digit in token))

def is_op(token: str) -> bool:
    return (token == '+' or
            token == '-' or
            token == '*' or token == 'x' or
            token == '/' or
            token == 'n' or
            token == 'c' or
#           token == 'p' or
            token == 'q')

# Syntactic processing (must be given valid syntax)
def div(s: Stack[int]) -> int:
    x = stack.pop(s)
    if x == 0:
        print('Division By 0 Error', file=STREAM)
    else:
        x = int((1 / x) * stack.pop(s))
    return x
        
def op(sym: str) -> Op:
    """ Generates genuine operators from syntactic forms.
        Operators only pop and cannot push to the stack. """
    op: Op
    if sym == '+':
        op = lambda s: stack.pop(s) + stack.pop(s)
    elif sym == '-':
        op = lambda s: -stack.pop(s) + stack.pop(s)
    elif sym == '*' or sym == 'x':
        op = lambda s: stack.pop(s) * stack.pop(s)
    elif sym == '/':
        op = div
    elif sym == 'n':
        op = lambda s: -stack.pop(s)
    elif sym == 'c':
        op = stack.empty
#   elif sym == 'p':
#       op = lambda s: print(s)
    elif sym == 'q':
        op = quit
    return op

def exp(sym: str) -> ExpAtom:
    """ Generates atomic RPN expressions """
    e: ExpAtom
    if is_op(sym):
        e = op(sym)
    else:
        e = int(sym)
    return e

# Semantic processing
def evaluate(s: Stack[int], e: Optional[Exp]) -> int:
    """ Evaluates RPN expressions and pushes them to the stack """
    result = stack.peek(s)
    if isinstance(e, int):
        result = stack.push(s, e)
    elif isinstance(e, list):
        if len(e) > 0:
            evaluate(s, e[0])
            result = evaluate(s, e[1:])
    elif e != None: # would be nice to typecheck this better,
        result = evaluate(s, cast(Op, e)(s)) # but casting is fine for now
    return result
        
# Main logic
def quit(s: Stack[int]) -> int:
    print(stack.pop(s), file=sys.stdout)
    if STREAM != sys.stdout:
        STREAM.close()
    sys.exit()
    return 0 # never happens, exists solely so evaluate() always returns int

def read(tokens: List[str]) -> Optional[Exp]:
    """ Parser and preprocessor, returns valid RPN syntax or None """
    result = None
    if not all(is_valid(t) for t in tokens):
        print('Syntax Error', file=STREAM)
    else:
        result = list(map(exp, tokens))
    return result

def repl(s: Stack[int]) -> None:
    """ Ye Olde Recursive REPL (maybe not the best idea for Python *shrug*) """
    try:
        syntax = tokenize(input(PROMPT))
    except EOFError:
        print('', file=STREAM)
        quit(s)
    print(str(evaluate(s, read(syntax))), file=STREAM)
    repl(s)

# Entry point
if len(sys.argv) > 1:
    if sys.argv[1] == '-q' or sys.argv[1] == '--quiet':
        PROMPT = ''
        STREAM = open('/dev/null', 'w')
    else:
        print('invalid options', file=sys.stderr)
        sys.exit(1)


repl(stack.new())
