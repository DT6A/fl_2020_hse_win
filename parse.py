import sys

import ply.yacc as yacc

from lex import tokens

class Node:
  def __init__(self, left, right, name):
    self.left = left
    self.right = right
    self.name = name


def pr(node):
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

def p_atom_tail(p):
  'atom : ID atomtail'
  p[0] = Node(Node(None, None, 'ID ' + p[1]), p[2], 'ATOM')

def p_tail(p):
  '''atomtail : atom
              | OBR atom CBR
              | OBR atom CBR atom
              '''
  if len(p) == 2:
    p[0] = p[1]
  elif len(p) == 4:
    p[0] = p[2]
  elif len(p) == 5:
    p[0] = Node(p[2], p[4], 'ATOM')
  else:
    pass

def p_error(p):
  if p == None:
    print("Missing dot at the end of the definition")
  else:
    print("Expected something different at line", p.lineno, 'col', p.lexpos)
  raise ValueError("Syntax error")


sys.stdout = open(sys.argv[1] + '.out', 'w')

parser = yacc.yacc()

with open(sys.argv[1], 'r') as inf:
  try:
    result = parser.parse(inf.read())
    print(pr(result))
  except ValueError:
    pass
