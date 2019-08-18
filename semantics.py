from rpn_h import *

def quit(s: Stack[int]) -> Stack[int]:
    print(stack.peek(s), file=sys.stdout)
    if STREAM != sys.stdout:
        STREAM.close()
    sys.exit()
    return s # never happens, present so evaluate() returns proper type

def div(s: Stack[int]) -> Stack[int]:
    result = s
    if stack.peek(s) == 0:
        print('Division By 0 Error', file=STREAM)
    else:
        x = int((1 / stack.peek(s)) * stack.peek(stack.pop(s)))
        result = stack.push(stack.pop(stack.pop(s)), x)
    return result
        
def exp(sym: str) -> Atom:
    """ Generates atomic RPN expressions from syntactic forms"""
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
        e = div
    elif sym == 'n':
        e = lambda s: stack.push(stack.pop(s), -stack.peek(stack.pop(s)))
    elif sym == 'c':
        e = lambda s: stack.new()
    elif sym == 'q':
        e = quit
    else:
        e = (lambda v: lambda s: stack.push(s, v))(int(sym))
    return e


