# -- imports --
from datetime import date, timedelta

# -- functions --
def lex(chars):
    return [("WordToken", chars)]

def parse(tokens):
    tok = tokens[0]
    return ("WordTree", tok[1])

def evaluate(tree):
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

def p(x):
    return parse(lex(x))

assert p("today") == ("WordTree", "today")
assert (
    p("tomorrow") ==
    ("WordTree", "tomorrow")
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

# -- main --
