from rpn_h import *

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
