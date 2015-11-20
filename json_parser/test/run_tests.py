#!/usr/bin/env python
from .. import JsonParser
import os

PATH = os.path.dirname(os.path.realpath(__file__))

def main():
    run_test('1.txt', [1, 2, 3, 4])
    run_test('2.txt', {'array': [1, 2, 3], 'message': 'hello'})

def run_test(filename, expected):
    test_file = open("%s/%s" % (PATH, filename), 'r')
    obj = JsonParser().parse("".join(line for line in test_file))
    assert obj == expected
    print "Test for file %s passed!" % filename
    test_file.close()

if __name__ == '__main__':
    main()
