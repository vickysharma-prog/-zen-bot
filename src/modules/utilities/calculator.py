"""A safe arithmetic evaluator for Zen-Bot.

Parses and evaluates a small arithmetic grammar (+, -, *, /, //, %, **, and
parentheses) using Python's ``ast`` module, so spoken sums like
"calculate 12 times 5 plus 3" can be answered without the security risk of
``eval``.
"""

from __future__ import annotations

import ast
import operator
import re

_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

# Spoken-word to symbol substitutions applied before parsing.
_WORDS = [
    (r"\bplus\b", "+"),
    (r"\bminus\b", "-"),
    (r"\btimes\b", "*"),
    (r"\bmultiplied by\b", "*"),
    (r"\bdivided by\b", "/"),
    (r"\bover\b", "/"),
    (r"\bmod(ulo)?\b", "%"),
    (r"\bto the power of\b", "**"),
    (r"\bsquared\b", "**2"),
    (r"\bx\b", "*"),
]


class CalculatorError(ValueError):
    pass


def normalize(expr: str) -> str:
    """Turn a spoken expression into a symbolic one."""
    expr = expr.lower()
    for pattern, repl in _WORDS:
        expr = re.sub(pattern, repl, expr)
    # keep only characters that belong in an arithmetic expression
    expr = re.sub(r"[^0-9+\-*/%.()\s]", " ", expr)
    return expr.strip()


def _eval(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise CalculatorError("only numbers are allowed")
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval(node.operand))
    raise CalculatorError("unsupported expression")


def evaluate(expr: str) -> float:
    """Evaluate an arithmetic expression (spoken or symbolic)."""
    cleaned = normalize(expr)
    if not cleaned:
        raise CalculatorError("nothing to calculate")
    try:
        tree = ast.parse(cleaned, mode="eval")
    except SyntaxError as exc:
        raise CalculatorError(f"could not parse: {expr}") from exc
    return _eval(tree.body)


def answer(expr: str) -> str:
    """Speech-friendly answer for a calculation request."""
    try:
        result = evaluate(expr)
    except CalculatorError as exc:
        return f"I couldn't calculate that: {exc}."
    # render whole numbers without a trailing .0
    if isinstance(result, float) and result.is_integer():
        result = int(result)
    return f"The answer is {result}."
