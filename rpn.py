import sys
from typing import List, Callable, Union, Optional, cast

import stack

# Constants and typedefs
PROMPT  = '> '
STREAM  = sys.stdout
Stack   = stack.Stack
ExpAtom = Callable[[Stack[int]], int]
Exp     = Union[ExpAtom, List[ExpAtom]]

# Pre-processing
def tokenize(entry: str) -> List[str]:
    return entry.split()

def is_valid(token: str) -> bool:
    return (token == '+' or
            token == '-' or
            token == '*' or token == 'x' or
            token == '/' or
            token == 'n' or
            token == 'c' or
#           token == 'p' or
            token == 'q' or
            all(ord(digit) > 47 and ord(digit) < 58 for digit in token))

# Syntactic processing (must be given valid syntax)
def div(s: Stack[int]) -> int:
    x = stack.pop(s)
    if x == 0:
        print('Division By 0 Error', file=STREAM)
    else:
        x = int((1 / x) * stack.pop(s))
    return stack.push(s, x)
        
def exp(sym: str) -> ExpAtom:
    """ Generates atomic RPN expressions from syntactic forms"""
    e: ExpAtom
    if sym == '+':
        e = lambda s: stack.push(s, stack.pop(s) + stack.pop(s))
    elif sym == '-':
        e = lambda s: stack.push(s, -stack.pop(s) + stack.pop(s))
    elif sym == '*' or sym == 'x':
        e = lambda s: stack.push(s, stack.pop(s) * stack.pop(s))
    elif sym == '/':
        e = div
    elif sym == 'n':
        e = lambda s: stack.push(s, -stack.pop(s))
    elif sym == 'c':
        e = stack.empty
#   elif sym == 'p':
#       e = lambda s: print(s)
    elif sym == 'q':
        e = quit
    else:
        e = (lambda v: lambda s: stack.push(s, v))(int(sym))
    return e

# Semantic processing
def evaluate(s: Stack[int], e: Optional[Exp]) -> int:
    """ Evaluates RPN expressions """
    result = stack.peek(s)
    if isinstance(e, list):
        if len(e) > 0:
            evaluate(s, e[0])
            result = evaluate(s, e[1:])
    elif e != None:
        result = cast(ExpAtom, e)(s)
    return result
        
# Main logic
def quit(s: Stack[int]) -> int:
    print(stack.pop(s), file=sys.stdout)
    if STREAM != sys.stdout:
        STREAM.close()
    sys.exit()
    return 0 # never happens, exists solely so evaluate() always returns int

def read(entry: str) -> Optional[Exp]:
    """ Parser and preprocessor, returns valid RPN syntax or None """
    result = None
    tokens = tokenize(entry)
    if not all(is_valid(t) for t in tokens):
        print('Syntax Error', file=STREAM)
    else:
        result = list(map(exp, tokens))
    return result

def repl(s: Stack[int]) -> None:
    """ Ye Olde Recursive REPL (maybe not the best idea for Python *shrug*) """
    try:
        print(str(evaluate(s, read(input(PROMPT)))), file=STREAM)
    except EOFError:
        print('', file=STREAM)
        quit(s)
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
