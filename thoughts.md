Idea 1 [X]
------
Would be interesting if all expressions---Including ints---were operators and
operators pushed to the stack. Then evaluate() would never explicitly interact
with the stack and would always return Exp(stack).

Example for getting Exp from int token
Exp(token) = (lambda val: lambda stack: push(stack, val))(int(token))

Would it simplify or confuse things? Evaluate() would be incredibly simple.
Idk if I want it that simple though. It might be too abstract.

---

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

---

No, now I'm pretty sure that this is the way it's supposed to work. The whole
point of RPN is that its semantics solely consists of stack operations.
Otherwise, I'd need an abstract syntax tree, and I'm starting to realize that
RPN and AST's are opposite methods of achieving the same goal. To try and
build out and evaluate an AST for an RPN evaluator makes no sense. I think the
allop method is the way to go for this semantics. If you want to build an AST,
do it for the next interpreter, not RPN.

RPN has no abstract syntax. That's kind of the point. Any expression just
evaluates to a series of pops and pushes. The syntax just encodes them.

Idea 2 [X]
------
Now that we're committed to this unified semantics, couldn't we make the whole
thing more functional by having evaluate return the stack rather than a value?
It might be a little more consistent, since the only datatype is the stack.
Evaluate should take a stack and return a stack. It doesn't know what a number
is, it only applies the expressions and returns the resulting stack.

This fits the repl model better. Though it's not really the most appropriate
implementation for Python. If you do a less functional version, evaluate should
control the stack and the expressions should just do arithmetic.

Idea 3 [ ]
------
I'd like to put the syntax down in BNF.
