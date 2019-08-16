RPN
===
This is a Reverse Polish Notation Calculator. You might think it's more complex
than it needs to be. That's because I built this as an exercise in designing a
a robust, reproducible, and extensible (if simple) language interpreter. RPN is
just the simplest syntax I could think of. That's why the logic, parsing, and
evaluation are separate, why everything is aggressively type-hinted, and why I
try to avoid "pythonic" code where possible.

The calculator is mostly meant to be used interactively, but it can also be fed
a file (through stdin). Each expression must be separated by whitespace and
computation stops at either a 'q' character or at EOF. The `--quiet` or `-q`
switch will suppress all output except for the final result.

At this time the calculator only handles integers.
  --Adon Shapiro
