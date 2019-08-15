RPN
===
This is a Reverse Polish Notation Calculator. You might think it's more complex
than it needs to be. That's because I tried to treat this as an exercise in
building not just a calculator, but a robust, reproducible, and extensible
(if simple) language interpreter. RPN is just the simplest syntax I could think
of. That's why the logic, parsing, and evaluation are separate, why everything
is aggressively type-hinted, and why I try to avoid "pythonic" code where
possible.

The calculator is mostly meant to be used interactively, but it can also be fed
a properly formatted file. Each number or operator must be on its own line, and
computation stops if a 'q' is read. The `--quiet` or `-q` options will suppress
all output except for the final result.

At this time the calculator only handles integers.
  --Adon Shapiro
