import sys  # import sys module

import ply.yacc as yacc  # import yacc

from lex import tokens  # import tokens from lex file


class Node: # AST node
  def __init__(self, left, right, name):  # initialization function
    self.left = left  # set left child
    self.right = right  # set right child
    self.name = name  # set node name


def pr(node):  # print AST
  a = node.name  # initialize string with node name
  if node.left != None:  # check if left child exists
    a += '(' + pr(node.left) + ')'  # get left child representation and add to the current one
  if node.right != None:  # check if right child exists
    a += '(' + pr(node.right) + ')'  # get right child representation and add to the current one
  return a  # return string


def p_defs_seq(p):  # parse sequence of definitions
  'seq : def DELIM seq'
  p[0] = Node(p[1], p[3], 'SEQ')  # create sequence node

def p_seq_def(p):  # parse the last definition
  'seq : def DELIM'
  p[0] = p[1]  # pass it through

def p_def_full(p):  # parse definition with head and body
  'def : atom CORK disj'
  p[0] = Node(p[1], p[3], 'DEF')  # create definition node

def p_def_head(p):  # parse definition without body
  'def : atom'
  p[0] = Node(p[1], None, 'DEF')  # create definition node

def p_disj_disj(p):  # parse disjunction
  'disj : conj OR disj'
  p[0] = Node(p[1], p[3], 'OR')  # create disjunction node

def p_disj_conj(p):  # parse disjunction as conjunction
  'disj : conj'
  p[0] = p[1]  # pass it through

def p_conj_conj(p):  # parse conjunction
  'conj : expr AND conj'
  p[0] = Node(p[1], p[3], 'AND')  # create conjunction

def p_conj_atom(p):  # parse conjunction as expression
  'conj : expr'
  p[0] = p[1]  # pass it through

def p_expr_disj(p):  # parse expression with brackets
  'expr : OBR disj CBR'
  p[0] = p[2]  # pass disjunction from inside through

def p_expr_atom(p):  # parse expression as atom
  'expr : atom'
  p[0] = p[1]  # pass it through


def p_atom_aseq(p):  # parse all atoms possible usages
  '''atom : ID atom
          | OBR atom CBR atom
          | OBR atom CBR
          | ID '''
  if len(p) == 3:  # sequence of ID and atom
    p[0] = Node(Node(None, None, 'ID ' + p[1]), p[2], 'ATOMSEQ')  # create atom sequence node with ID node inside
  elif len(p) == 4:  # last atom at subexpression inside of the brackets
    p[0] = p[2]  # extract atom from brackets
  elif len(p) == 5:  # sequence of atoms where the first one is inside of the brackets
    p[0] = Node(p[2], p[4], 'ATOMSEQ')  # create node of atoms sequence extracting the first one
  else:  # last ID at subexpression
    p[0] = Node(None, None, 'ID ' + p[1])  # create ID node


def p_error(p):  # process parsing error
  if p == None:  # p is the last token
    print("Missing dot at the end of the definition")  # print error message
  else:  # p is not at the end
    print("Expected something different at line", p.lineno, 'col', p.lexpos)  # print error message
  raise ValueError("Syntax error")  # raise exception to stop parsing


sys.stdout = open(sys.argv[1] + '.out', 'w')  # redirect standart output to the file

parser = yacc.yacc()  # create parser

with open(sys.argv[1], 'r') as inf:  # open input file
  try:  # try to parse file
    result = parser.parse(inf.read())  # get file content and process it
    print(pr(result))  # print AST
  except ValueError:  # catch exception
    pass  # ignore it
