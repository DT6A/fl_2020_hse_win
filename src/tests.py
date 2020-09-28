import os

from static_analyzer import analyze_file

TESTS_PATH = 'test_files'

test_files = os.listdir(TESTS_PATH)

for fn in test_files:
    print("FILE:", fn)
    res = analyze_file(TESTS_PATH + '/' + fn)
    if fn[0] == 'c' and res == False or fn[0] == 'i' and res == True:
        print("INCORRECT RESULT FOR FILE", fn)
    print()