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
