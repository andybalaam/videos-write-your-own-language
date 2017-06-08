# -- imports --
from datetime import date, timedelta

# -- functions --
def make_token(s):
    if s[0] in "0123456789":
        return ("NumberToken", s)
    elif s[0] in "+":
        return ("OperatorToken", s[0])
    else:
        return ("WordToken", s)

def lex(chars):
    return [
        make_token(s)
        for s in chars.split(" ")
    ]

def parse(tokens, so_far=None):
    if len(tokens) == 0:
        return so_far
    tok = tokens[0]
    other_toks = tokens[1:]
    if tok[0] == "NumberToken":
        next_tok = tokens[1]
        return ("LengthTree", tok[1], next_tok[1])
    elif tok[0] == "OperatorToken":
        return ("OperatorTree",
            tok[1], so_far, parse(other_toks))
    else: # Must be WordToken
        return parse(
            other_toks, ("WordTree", tok[1]))

def length_tree_in_days(length_tree):
    number = int(length_tree[1])
    unit = length_tree[2]
    if unit == "weeks":
        return number * 7
    else:
        return number

def evaluate(tree):
    if tree[0] == "LengthTree":
        return (
            "LengthValue",
            length_tree_in_days(tree)
        )
    elif tree[0] == "OperatorTree":
        left = evaluate(tree[2])
        right = evaluate(tree[3])
        return (
            "DateValue",
            left[1] + timedelta(days=right[1])
        )
    elif tree[0] == "WordTree":
        if tree[1] == "today":
            return ("DateValue", date.today())
        elif tree[1] == "tomorrow":
            return (
                "DateValue",
                date.today() + timedelta(days=1)
            )

# -- tests --
assert lex("today") == [("WordToken", "today")]
assert (
    lex("tomorrow") ==
    [("WordToken", "tomorrow")]
)
assert (
    lex("2 days") ==
    [
        ("NumberToken", "2"),
        ("WordToken", "days")
    ]
)
assert (
    lex("3 weeks") ==
    [
        ("NumberToken", "3"),
        ("WordToken", "weeks")
    ]
)
assert (
    lex("today + 3 days") ==
    [
        ("WordToken", "today"),
        ("OperatorToken", "+"),
        ("NumberToken", "3"),
        ("WordToken", "days")
    ]
)

def p(x):
    return parse(lex(x))

assert p("today") == ("WordTree", "today")
assert (
    p("tomorrow") ==
    ("WordTree", "tomorrow")
)
assert (
    p("2 days") ==
    ("LengthTree", "2", "days")
)
assert (
    p("3 weeks") ==
    ("LengthTree", "3", "weeks")
)
assert (
    p("today + 3 days") ==
    ("OperatorTree",
        "+",
        ("WordTree", "today"),
        ("LengthTree", "3", "days")
    )
)

def e(x):
    return evaluate(parse(lex(x)))

today = date.today()

def days(n):
    return timedelta(days=n)

assert e("today") == ("DateValue", today)
assert (
    e("tomorrow") ==
    ("DateValue", today + days(1))
)
assert e("2 days") == ("LengthValue", 2)
assert e("3 weeks") == ("LengthValue", 21)
assert (
    e("today + 3 days") ==
    ("DateValue", today + days(3))
)
assert (
    e("tomorrow + 1 day") ==
    ("DateValue", today + days(2))
)

# -- main --
