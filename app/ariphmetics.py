import re


def filter_arithmetic_expression(arithmetic_expression: str) -> str:
    operations: tuple = ("+", "-", "*", "/")

    # Define the regular expression pattern for splitting the string
    pattern = r"[\s\d]+|[+\-*/()]"

    # Split the string using the pattern
    request = re.findall(pattern, arithmetic_expression)
    for i in request:
        request[request.index(i)] = request[request.index(i)].replace(" ", "")
    for i in request:
        if i.isdigit() or i in operations:
            continue
        else:
            index = request.index(i)
            request[index] = f'"{i}"'
    try:
        result = eval("".join(request))
    except Exception as e:
        print(e)
        result = str(e)

    if arithmetic_expression.startswith("$(") and arithmetic_expression.endswith(")"):
        return result
    else:
        return arithmetic_expression
