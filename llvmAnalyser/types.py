import re

vector = re.compile(r'<(vscale x )?[0-9]* x (?:i[1-9][0-9]*|half|bfloat|float|double|fp128|x86_FP80|ppc_fp128|.*\*)>')


# this function takes a chain of tokens of which the type has to start in the first token
# it will return the entire type that is specified along with the remaining tokens
def get_type(tokens):
    if "\"" in tokens[0]:
        return get_string_type(tokens)

    if tokens[0][0] == "{" or tokens[0][1] == "{":
        return get_struct_type(tokens)

    if tokens[0][0] == "<":
        return get_vector_type(tokens)

    if tokens[0][0] == "[":
        return get_array_type(tokens)

    specified_type = tokens[0]
    tokens.pop(0)

    # register end of type
    if specified_type[-1] == "," and specified_type.count("(") == specified_type.count(")"):
        specified_type = specified_type[:-1]
        return specified_type, tokens

    if specified_type[-1] == ")" and specified_type.count("(") + 1 == specified_type.count(")"):
        specified_type = specified_type[:-1]
        return specified_type, tokens

    if len(tokens) >= 5 and tokens[0][:5] == "(...)":
        return specified_type, tokens

    return check_for_templated_parts(specified_type, tokens)


# check if the type that is discovered at this point is the return type of a function type
def check_for_function_type(specified_type, tokens):
    if (len(tokens) == 0 or "(" not in tokens[0]) and specified_type.count("(") == specified_type.count(")"):
        if specified_type[-1] == ",":
            specified_type = specified_type[:-1]
        return specified_type, tokens

    if tokens[0].split("(")[0] not in {"", "*"} and tokens[0].count("(") != 0:
        if specified_type[-1] == ",":
            specified_type = specified_type[:-1]
        return specified_type, tokens

    open_counter = specified_type.count("(") - specified_type.count(")")
    while True:
        open_counter += tokens[0].count("(")
        open_counter -= tokens[0].count(")")
        specified_type += " {}".format(tokens[0])
        tokens.pop(0)
        if open_counter <= 0:
            if specified_type[-1] == ",":
                specified_type = specified_type[:-1]
            if specified_type[-1] == ")" and open_counter < 0:
                specified_type = specified_type[:-1]
            return specified_type, tokens


# check if the type that is discovered at this point is a pointer to said type
def check_for_pointer_type(specified_type, tokens):
    if len(tokens) == 0:
        if specified_type[-1] == ",":
            specified_type = specified_type[:-1]
        return specified_type, tokens
    if "*" not in tokens[0] or ("(" in tokens[0] and tokens[0].count("(") != tokens[0].count(")")):
        return check_for_function_type(specified_type, tokens)

    elif tokens[0].count("(") == tokens[0].count(")") and "*" not in tokens[0].rsplit(")", 1)[-1]:
        return check_for_function_type(specified_type, tokens)

    temp_tokens = tokens[0].rsplit("*", 1)
    tokens.pop(0)

    specified_type += " {}*".format(temp_tokens[0])
    return check_for_function_type(specified_type, tokens)


def check_for_templated_parts(specified_type, tokens):
    if len(tokens) == 0:
        if specified_type[-1] == ",":
            specified_type = specified_type[:-1]
        return specified_type, tokens

    open_counter = specified_type.count("<") - specified_type.count(">")
    while open_counter != 0:
        open_counter += tokens[0].count("<")
        open_counter -= tokens[0].count(">")
        specified_type += " {}".format(tokens[0])
        tokens.pop(0)

    return check_for_pointer_type(specified_type, tokens)


# check if the base type is a vector type
def get_vector_type(tokens):
    if "<" not in tokens[0] or "{" in tokens[0]:
        return None

    specified_type = tokens[0]
    tokens.pop(0)
    while True:
        if vector.match(specified_type):
            return check_for_pointer_type(specified_type, tokens)
        specified_type += " {}".format(tokens[0])
        tokens.pop(0)


# check if the base type is an array type
def get_array_type(tokens):
    if "[" not in tokens[0]:
        return None

    specified_type = tokens[0]
    tokens.pop(0)
    open_counter = 1
    while True:
        open_counter += tokens[0].count("[")
        open_counter -= tokens[0].count("]")
        specified_type += " {}".format(tokens[0])
        tokens.pop(0)
        if open_counter == 0:
            return check_for_pointer_type(specified_type, tokens)


# check if the base type is a struct type
def get_struct_type(tokens):
    if "{" not in tokens[0]:
        return None

    specified_type = tokens[0]
    tokens.pop(0)
    while True:
        specified_type += " {}".format(tokens[0])
        tokens.pop(0)
        if "}" in specified_type:
            return check_for_pointer_type(specified_type, tokens)


# check if the type is a type specified in string
def get_string_type(tokens):
    if "\"" not in tokens[0]:
        return None

    specified_type = tokens[0]
    tokens.pop(0)
    while True:
        if specified_type.count("\"") == 2:
            if specified_type[-1] == ")" and specified_type.count("(") + 1 == specified_type.count(")"):
                specified_type = specified_type[:-1]
            return check_for_function_type(specified_type, tokens)
        specified_type += " {}".format(tokens[0])
        tokens.pop(0)
