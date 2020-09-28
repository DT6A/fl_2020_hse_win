import sys

from lex import tokenize_file, t2w



class Node:
    def __init__(self, left, right, name):
        self.left = left
        self.right = right
        self.name = name


class Parser:
    def __init__(self, tokens):
        self.current = next(tokens)
        self.prev = None
        self.tokens = tokens

    def accept(self, tok):
        if self.current == '0':
            return False
        if self.current.type == tok:
            self.prev = self.current
            self.current = next(self.tokens)
            return True
        return False

    def expect(self, tok):
        if self.current.type == tok:
            self.prev = self.current
            self.current = next(self.tokens)
            return True
        print("Expected closing bracket but got", t2w(self.current.type), "at line", self.current.lineno, "col", self.current.lexpos)
        raise ValueError()
        #print("Unexpected token", self.current.type, "expected", tok)
        return False

    def log_error(self, token, expected):
        if token == '0':
            print("Expected", expected, "but got", "EOF", "after line", self.prev.lineno, "col", self.prev.lexpos)
            raise ValueError()
        print("Expected", expected, "but got", t2w(token.type), "at line", token.lineno, "col", token.lexpos)
        raise ValueError()


    def id(self):
        token = self.current
        self.prev = self.current
        self.current = next(self.tokens)
        if token.type != "ID":
            self.log_error(token, "id")
            return None
        return Node(None, None, token.value)

    def expr(self):
        if self.accept('OBR'):
            r = self.disj()
            if self.expect('CBR'):
                return r
            return None
        token = self.current
        self.current = next(self.tokens)
        if token.type != "ID":
            self.log_error(token, "id or expression")
            return None
        return Node(None, None, token.value)

    def conj(self):
        l = self.expr()
        if self.accept('AND'):
            r = self.conj()
            if r == None:
                self.log_error(self.current, "expression")
                return None
            return Node(l, r, "and")
        return l

    def disj(self):
        l = self.conj()
        if self.accept('OR'):
            r = self.disj()
            if r == None:
                self.log_error(self.current, "expression")
                return None
            return Node(l, r, "or")
        return l

    def R(self):
        l = self.id()
        if self.accept('CORK'):
            r = self.disj()
            if r == None:
                return None
            if not self.accept('DELIM'):
                self.log_error(self.current, "dot")
                return None
            return Node(l, r, "def")
        if not self.accept('DELIM'):
            self.log_error(self.current, "dot")
            return None
        return l

    def rel(self):
        l = self.R()
        if self.current == '0':
            return l
        r = self.rel()
        if r == None:
            return l
        return Node(l, r, 'seq')


def lexer(s):
    for c in s:
        yield c

    while True:
        yield '0'

def pr(node):
    a = "("
    if node.left!=None:
        a += pr(node.left)
    a += " " + node.name + " "
    if node.right != None:
        a += pr(node.right)
    a+=')'
    return a

def analyze_file(file_name):
    lexer.__eof_pos = None
    no_errs, tokens = tokenize_file(file_name)
    if not no_errs:
        print("Program is incorrect. Illegal character(s) in input file.")
        return False
    if (len(tokens) == 0):
        print("Empty file")
        return True
    p = Parser(lexer(tokens))
    try:
        tree = p.rel()
    except:
        print("Failed to parse")
        return False

    print("Program is correct.")
    print(pr(tree))
    return True
