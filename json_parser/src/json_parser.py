#!/usr/bin/env python
"""
JSON Parser.

Based on lis.py: http://norvig.com/lis.py
"""

import re
import sys

STRUCTURAL_CHARS = ['[', ']', '{', '}', ':', ',']

def expect(expected, actual):
    """ Throws a syntax error if parameters don't match. """
    if expected != actual:
        raise SyntaxError("Expected %s, found %s" % (expected, actual))

class JsonParser(object):
    """
    Json Parser
    """
    def __init__(self):
        self.line = 0
        self.col = 0

    def parse(self, json):
        """ Parses a JSON string. """
        return self.read_from(self.tokenize(json))

    @staticmethod
    def tokenize(json):
        """ Converts a string into tokens. """
        for char in STRUCTURAL_CHARS:
            json = json.replace(char, " %s " % char)
        return re.split(r'[ |\t|\n|\r]+', json.strip())

    def read_from(self, tokens):
        """ Deserializes tokens into Python objects. """
        if len(tokens) == 0:
            raise SyntaxError('Unexpected EOF while reading!')

        token = tokens.pop(0)

        if token == '[':
            return self.read_array(tokens)
        elif token == '{':
            return self.read_map(tokens)
        elif token in [']', '}', ',']:
            raise SyntaxError('Unexpected %s' % token)
        else:
            return self.read_atom(token)

    def read_array(self, tokens):
        """ Parses tokens into an array. """
        array = []
        first = True

        while tokens[0] != ']':
            if first:
                first = False
            else:
                expect(tokens.pop(0), ',')
            array.append(self.read_from(tokens))
        expect(tokens.pop(0), ']')
        return array

    def read_map(self, tokens):
        """ Parses tokens into a map. """
        obj = {}
        first = True

        while tokens[0] != '}':
            if first:
                first = False
            else:
                expect(tokens.pop(0), ',')
            key = tokens.pop(0)
            expect(tokens.pop(0), ':')
            obj[key] = self.read_from(tokens)
        expect(tokens.pop(0), '}')
        return obj

    @staticmethod
    def read_atom(token):
        """ Parses the value of an atomic token. """
        try:
            return int(token)
        except ValueError:
            try:
                return float(token)
            except ValueError:
                if token[0:1] == token[-1:] == '"':
                    return str(token[1:-1])

def main():
    """ Main loop """
    print JsonParser().parse("".join([line for line in sys.stdin]))

if __name__ == '__main__':
    main()

