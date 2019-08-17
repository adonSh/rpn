Idea 1
------
Would be interesting if all expressions---Including ints---were operators and
operators pushed to the stack. Then evaluate() would never explicitly interact
with the stack and would always return Exp(stack).

Example for getting Exp from int token
Exp(token) = (lambda val: lambda stack: push(stack, val))(int(token))

Would it simplify or confuse things? Evaluate() would be incredibly simple.
Idk if I want it that simple though. It might be too abstract.

Ok I so I implemented this and I'm not sure what to think. It has some
interesting semantic implications. Any expression is merely something to be
done with the stack, meaning an int is not an int, it's a push operation. This
logic works for RPN, and is maybe worth exploring, but It might defeat the
purpose of the exercise a litte to only have one abstract datatype. Or maybe
not? I guess the bones are still sound for building out to a more complex
syntax. Is this just a distillation of RPN?

Now I'm thinking I don't like it makes the abstract and concrete syntax
inconsistent. The concrete data types include ints and ops (and maybe cmds),
but the only data type the abstract syntax has a notion of is the stack.

Yeah, that's it. I took it halfway there with the ops working on the stack, and
this took it all the way there, and now I'm pretty sure I want to go all the
way back.

Idea 2
------
I'd like to put the abstract syntax down in BNF.
