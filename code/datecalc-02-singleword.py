# -- imports --
from datetime import date, timedelta

# -- functions --
def lex(chars):
    return [("WordToken", chars)]

def parse(tokens):
    tok = tokens[0]
    return ("WordTree", tok[1])

def evaluate(tree):
    return ("DateValue", date.today())

# -- tests --
assert lex("today") == [("WordToken", "today")]

def p(x):
    return parse(lex(x))

assert p("today") == ("WordTree", "today")

def e(x):
    return evaluate(parse(lex(x)))

today = date.today()

assert e("today") == ("DateValue", today)

# -- main --
