#!/usr/bin/env python
"""
JSON Parser.

Based on lis.py: http://norvig.com/lis.py
"""

import re
import sys

STRUCTURAL_CHARS = ['[', ']', '{', '}', ':', ',']

def parse(json):
    """
    Parses a JSON string.
    """
    return read_from(tokenize(json))

def tokenize(json):
    """
    Converts a string into tokens.
    """
    for char in STRUCTURAL_CHARS:
        json = json.replace(char, " %s " % char)
    return re.split(r'[ |\t|\n|\r]+', json.strip())

def read_from(tokens):
    """
    Deserializes tokens into Python objects.
    """
    if len(tokens) == 0:
        raise SyntaxError('Unexpected EOF while reading!')

    token = tokens.pop(0)

    if token == '[':
        lst = []
        first = True

        while tokens[0] != ']':
            if first:
                first = False
            else:
                assert tokens.pop(0) == ','
            lst.append(read_from(tokens))
        assert tokens.pop(0) == ']'
        return lst
    elif token == '{':
        obj = {}
        first = True

        while tokens[0] != '}':
            if first:
                first = False
            else:
                assert tokens.pop(0) == ','
            key = tokens.pop(0)
            assert tokens.pop(0) == ':'
            obj[key] = read_from(tokens)
        assert tokens.pop(0) == '}'
        return obj

    elif token == ']':
        raise SyntaxError('Unexpected ]')
    elif token == '}':
        raise SyntaxError('Unexpected }')
    elif token == ',':
        raise SyntaxError('Unexpected ,')
    else:
        return atom(token)

def atom(token):
    """
    Parses the value of an atomic token.
    """
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            if token[0:1] == token[-1:] == '"':
                return str(token[1:-1])

def main():
    """
    Main loop
    """
    text = ""
    for line in sys.stdin:
        text += line

    print parse(text)

main()
