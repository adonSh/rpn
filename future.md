Idea 1
------
Would be interesting if all expressions---Including ints---were operators and
operators pushed to the stack. Then evaluate() would never explicitly interact
with the stack and would always return Exp(stack).

Example for getting Exp from int token
Exp(token) = (lambda val: lambda stack: push(stack, val))(int(token))

Would it simplify or confuse things? Evaluate() would be incredibly simple.
Idk if I want it that simple though. It might be too abstract. It would be fun
to try though :)

Idea 2
------
I'd like to put the abstract syntax down in BNF.

Idea 3
------
Think about whether it makes more sense for read() to call tokenize() as a
subroutine or if it should take tokenize()'s output as input (current
implementation).
