import ply.lex as lex 
import sys

sys.stdout = open(sys.argv[1] + '.out', 'w')

reserved = {
  'module': 'MODULE',
  'sig': 'SIG',
  'type': 'TYPE'
}

tokens = [
  'NUM', 
  'IMPL',
  'CORK',
  'ID',
  'DELIM',
  'STR'
] + list(reserved.values())

def t_ID(t):
  r'[a-zA-Z_][a-zA-Z_0-9]*'
  t.type = reserved.get(t.value, 'ID')
  return t

def t_NUM(t): 
  r'[0-9]+'
  t.value = int(t.value)
  return t

def t_STR(t):
  r'\".*?\"'
  t.value = str(t.value)
  return t

t_IMPL = r'\-\>'
t_CORK = r'\:\-'
t_DELIM = r'\,|\.|\[|\]|\|'

t_ignore = ' \t'

def update_lex_pos(tok):
  if tok.lineno != update_lex_pos.prev_line:
    update_lex_pos.pos_subst = update_lex_pos.prev_tok_pos
    update_lex_pos.prev_line = tok.lineno
  update_lex_pos.prev_tok_pos = tok.lexpos + len(str(tok.value))
update_lex_pos.prev_tok_pos = 0
update_lex_pos.pos_subst = 0
update_lex_pos.prev_line = 1

def t_newline(t): 
  r'\n+'
  t.lexer.lineno += len(t.value)
  update_lex_pos(t)


def t_error(t):
  t.value = t.value[0]
  update_lex_pos(t)
  print("Illegal character '%s' at line %i pos %i" % (t.value, t.lineno, t.lexpos - update_lex_pos.pos_subst))
  t.lexer.skip(1)

lexer = lex.lex() 

with open(sys.argv[1], 'r') as inf:
  lexer.input(inf.read())

while True:
  tok = lexer.token() 
  if not tok: 
    break
  update_lex_pos(tok)
  tok.lexpos -= update_lex_pos.pos_subst
  print(', '.join(list(map(str,[tok.type, tok.value, tok.lineno, tok.lexpos]))))
