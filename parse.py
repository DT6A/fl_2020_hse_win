import sys

import ply.yacc as yacc

from lex import tokens

class Node:
  def __init__(self, left, right, name):
    self.left = left
    self.right = right
    self.name = name


def pr(node):
  #if type(node) == str:
    #return node
  a = node.name
  if node.name == "DEF":
    a = '\n' + a
  if node.left != None:
    a += '(' + pr(node.left) + ')'
  if node.right != None:
    a += '(' + pr(node.right) + ')'
  return a


def p_defs_seq(p):
  'seq : def DELIM seq'
  p[0] = Node(p[1], p[3], 'SEQ')

def p_seq_def(p):
  'seq : def DELIM'
  p[0] = p[1]

def p_def_full(p):
  'def : atom CORK disj'
  p[0] = Node(p[1], p[3], 'DEF')

def p_def_head(p):
  'def : atom'
  p[0] = Node(p[1], None, 'DEF')

def p_disj_disj(p):
  'disj : conj OR disj'
  p[0] = Node(p[1], p[3], 'OR')

def p_disj_conj(p):
  'disj : conj'
  p[0] = p[1]

def p_conj_conj(p):
  'conj : expr AND conj'
  p[0] = Node(p[1], p[3], 'AND')

def p_conj_atom(p):
  'conj : expr'
  p[0] = p[1]

def p_expr_disj(p):
  'expr : OBR disj CBR'
  p[0] = p[2]

def p_expr_atom(p):
  'expr : atom'
  p[0] = p[1]

def p_atom_id(p):
  'atom : ID'
  p[0] = Node(None, None, 'ID ' + p[1])

def p_atom_atom(p):
  'atom : ID atom'
  p[0] = Node(Node(None, None, 'ID ' + p[1]), p[2], 'ATOM')

def p_atom_tail(p):
  'atom : ID atomproxy'
  p[0] = Node(Node(None, None, 'ID ' + p[1]), p[2], 'ATOMSEQ')

def p_atom_tail_tail(p):
  'atom : ID atomproxy atom'
  p[0] = Node(Node(Node(None, None, 'ID ' + p[1]), p[2], 'ATOM'), p[3], 'ATOMSEQ')

def p_atom_tail_proxy(p):
  'atom : ID atomproxy atomproxy'
  p[0] = Node(Node(Node(None, None, 'ID ' + p[1]), p[2], 'ATOM'), p[3], 'ATOMSEQ')

def p_proxy_proxy(p):
  'atomproxy : OBR atomproxy2 CBR'
  p[0] = p[2]

def p_proxy_atom(p):
  'atomproxy2 : atom'
  p[0] = p[1]

def p_proxy_proxy2(p):
  'atomproxy2 : OBR atomproxy2 CBR'
  p[0] = p[2]


def p_error(p):
  if p == None:
    print("Missing dot at the end of the definition")
  else:
    print("Expected something different at line", p.lineno, 'col', p.lexpos)
  raise ValueError("Syntax error")



parser = yacc.yacc()

'''
while True:
  try:
    s = input("calc> ")
  except EOFError:
    break
  if not s:
    continue
  try:
    result=parser.parse(s)
    print(pr(result))
  except:
    pass
'''
sys.stdout = open(sys.argv[1] + '.out', 'w')

with open(sys.argv[1], 'r') as inf:
  try:
    result = parser.parse(inf.read())
    print(pr(result))
  except ValueError:
    pass
