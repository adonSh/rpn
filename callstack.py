def is_op(sym):
    return sym == '+' or sym == '-'

def binop(op, x, y):
    ops = {
        '+': lambda a, b: b + a,
        '-': lambda a, b: b - a,
    }
    val = ops[op](x, y)
    print(str(val))
    return calc(input('> '))(val)

def calc(exp):
    if is_op(exp):
        r = lambda x: lambda y: binop(exp, x, y)
    else:
        r = calc(input('> '))(int(exp))
    return r
calc(input('> '))
