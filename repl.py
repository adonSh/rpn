from rpn_h import *
import parser
import semantics

def evaluate(expr: Optional[Exp], env: Env) -> Stack[int]:
    """ Evaluates RPN expressions """
    result = env
    if isinstance(expr, list):
        if len(expr) > 0:
            result = evaluate(expr[1:], evaluate(expr[0], env))
    elif expr != None:
        result = cast(Atom, expr)(env)
    return result
        
def read(entry: str) -> Optional[Exp]:
    """ Parser and preprocessor, returns semantic RPN expression or None """
    result = None
    tokens = parser.tokenize(entry)
    if not all(parser.is_valid(t) for t in tokens):
        print('Syntax Error', file=sys.stderr)
    else:
        result = list(map(semantics.exp, tokens))
    return result

def repl(env: Env) -> None:
    """ Ye Olde Recursive REPL """
    try:
        newenv = evaluate(read(input(PROMPT)), env)
        print(str(stack.peek(newenv)), file=STREAM)
    except EOFError:
        print('', file=STREAM)
        quit(env)
    repl(newenv)
