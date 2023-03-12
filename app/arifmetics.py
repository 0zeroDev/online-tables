import re


def is_formula(expression: str) -> bool:
    return expression.startswith("$(") and expression.endswith(")")


def calculate_expression(expression: str) -> str:
    """
    Returns result of arifmetic calculations if expression inside $().

    Example:
    >>> calculate_expression('2 + 3')
    ... 2 + 3
    >>> calculate_expression('$(2 + 3)')
    ... 5
    """
    calculated: str

    if is_formula(expression):
        try:
            print(f'to calculate: {filter(expression)}')
            calculated = eval(filter(expression))
        except Exception as error:
            print(f'ERROR while trying to calculate expression.\n|->{error}')
            calculated = expression
    else:
        calculated = expression

    return calculated


def filter(expression: str) -> str:
    """
    Returns filtered expression which we can use in eval().
    """

    # slice [2:-1] removes $() from formula
    expression = expression[2:-1].replace(' ', '')
    operations: str = "([-+*/()])"

    operands: list[str] = re.split(operations, expression)
    print(operands)
    for operand in operands:
        if operand.isdigit() or operand in operations:
            continue
        else:
            expression = expression.replace(operand, f'\'{operand}\'')

    return expression
