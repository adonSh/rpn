import sys
from typing import List, Callable, Union, Optional, cast

import intstack as stack

# Constants and typedefs
PROMPT  = '> '
STREAM  = sys.stdout
Stack   = stack.Stack
Env     = Stack[int]
Atom    = Callable[[Stack[int]], Stack[int]]
Exp     = Union[Atom, List[Atom]]

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
def div(s: Stack[int]) -> Stack[int]:
    result = s
    if stack.peek(s) == 0:
        print('Division By 0 Error', file=STREAM)
    else:
        x = int((1 / stack.peek(s)) * stack.peek(stack.pop(s)))
        result = stack.push(stack.pop(stack.pop(s)), int((1 / stack.peek(s)) * stack.peek(stack.pop(s))))
    return result
        
def exp(sym: str) -> Atom:
    """ Generates atomic RPN expressions from syntactic forms"""
    e: Atom
    if sym == '+':
        e = lambda s: stack.push(stack.pop(stack.pop(s)), stack.peek(s) + stack.peek(stack.pop(s)))
    elif sym == '-':
        e = lambda s: stack.push(stack.pop(stack.pop(s)), -stack.peek(s) + stack.peek(stack.pop(s)))
    elif sym == '*' or sym == 'x':
        e = lambda s: stack.push(stack.pop(stack.pop(s)), stack.peek(s) * stack.peek(stack.pop(s)))
    elif sym == '/':
        e = div
    elif sym == 'n':
        e = lambda s: stack.push(stack.pop(s), -stack.peek(stack.pop(s)))
    elif sym == 'c':
        e = lambda s: stack.new()
#   elif sym == 'p':
#       e = stack.print
    elif sym == 'q':
        e = quit
    else:
        e = (lambda v: lambda s: stack.push(s, v))(int(sym))
    return e

# Semantic processing
def evaluate(expr: Optional[Exp], env: Env) -> Stack[int]:
    """ Evaluates RPN expressions """
    result = env
    if isinstance(expr, list):
        if len(expr) > 0:
            result = evaluate(expr[1:], evaluate(expr[0], env))
    elif expr != None:
        result = cast(Atom, expr)(env)
    return result
        
# Main logic
def quit(s: Stack[int]) -> Stack[int]:
    print(stack.peek(s), file=sys.stdout)
    if STREAM != sys.stdout:
        STREAM.close()
    sys.exit()
    return s # never happens, present so evaluate() returns proper type

def read(entry: str) -> Optional[Exp]:
    """ Parser and preprocessor, returns valid RPN syntax or None """
    result = None
    tokens = tokenize(entry)
    if not all(is_valid(t) for t in tokens):
        print('Syntax Error', file=sys.stderr)
    else:
        result = list(map(exp, tokens))
    return result

def repl(env: Env) -> None:
    """ Ye Olde Recursive REPL (maybe not the best idea for Python *shrug*) """
    try:
        newenv = evaluate(read(input(PROMPT)), env)
        print(str(stack.peek(newenv)), file=STREAM)
    except EOFError:
        print('', file=STREAM)
        quit(env)
    repl(newenv)

# Entry point
if len(sys.argv) > 1:
    if sys.argv[1] == '-q' or sys.argv[1] == '--quiet':
        PROMPT = ''
        STREAM = open('/dev/null', 'w')
    else:
        print('invalid options', file=sys.stderr)
        sys.exit(1)

repl(stack.new())
