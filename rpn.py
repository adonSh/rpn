import sys
from typing import List, Callable, Union, Optional, cast

import intstack as stack

# Constants and typedefs
PROMPT = '> '
STREAM = sys.stdout
Stack  = stack.Stack
Atom   = Callable[[Stack[int]], Stack[int]]
Exp    = Union[Atom, List[Atom]]

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
            token == 'q' or
            all(ord(digit) > 47 and ord(digit) < 58 for digit in token))

# Semantics
def quit(s: Stack[int]) -> Stack[int]:
    print(stack.peek(s), file=sys.stdout)
    STREAM.close()
    sys.exit()
    return s # never happens, but allows evaluate() to return proper type

def exp(sym: str) -> Atom:
    """ Generates semantics from RPN expressions """
    e: Atom
    if sym == '+':
        e = lambda s: stack.push(stack.pop(stack.pop(s)),
                                 stack.peek(s) + stack.peek(stack.pop(s)))
    elif sym == '-':
        e = lambda s: stack.push(stack.pop(stack.pop(s)),
                                 -stack.peek(s) + stack.peek(stack.pop(s)))
    elif sym == '*' or sym == 'x':
        e = lambda s: stack.push(stack.pop(stack.pop(s)),
                                 stack.peek(s) * stack.peek(stack.pop(s)))
    elif sym == '/':
        def div(s: Stack[int]) -> Stack[int]:
            result = s
            if stack.peek(s) == 0:
                print('Division By 0 Error', file=STREAM)
            else:
                x = int((1 / stack.peek(s)) * stack.peek(stack.pop(s)))
                result = stack.push(stack.pop(stack.pop(s)), x)
            return result
        e = div
    elif sym == 'n':
        e = lambda s: stack.push(stack.pop(s), -stack.peek(s))
    elif sym == 'c':
        e = lambda s: stack.new()
    elif sym == 'q':
        e = quit
    else:
        e = (lambda v: lambda s: stack.push(s, v))(int(sym))
    return e

# Main logic
def evaluate(expr: Optional[Exp], stk: Stack[int]) -> Stack[int]:
    """ Applies semantic expressions and returns the resulting stack """
    result = stk
    if isinstance(expr, list):
        if len(expr) > 0:
            result = evaluate(expr[1:], evaluate(expr[0], stk))
    elif expr != None:
        result = cast(Atom, expr)(stk)
    return result
        
def read(entry: str) -> Optional[Exp]:
    """ Parser and preprocessor. Since RPN has no abstract syntax I have read()
        go ahead and return the actual semantics for each expression. """
    result = None
    tokens = tokenize(entry)

    if not all(is_valid(t) for t in tokens):
        print('Syntax Error', file=sys.stderr)
    else:
        result = list(map(exp, tokens))

    return result

def repl(stk: Stack[int]) -> None:
    """ Ye Olde Recursive REPL """
    try:
        newstk = evaluate(read(input(PROMPT)), stk)
    except EOFError:
        print('', file=STREAM)
        quit(stk)

    print(str(stack.peek(newstk)), file=STREAM)
    repl(newstk)

# Entry point
if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '-q' or sys.argv[1] == '--quiet':
            PROMPT = ''
            STREAM = open('/dev/null', 'w')
        else:
            print('invalid options', file=sys.stderr)
            sys.exit(1)

    repl(stack.new())
