import ply.lex as lex


tokens = [
  'CORK',
  'ID',
  'DELIM',
  'AND',
  'OR',
  'OBR',
  'CBR'
]

t2w_d = {
    'CORK': ':-',
    'ID': 'id',
    'DELIM': '.',
    'OBR': '(',
    'CBR': ')'
}

def t2w(t):
    if t in t2w_d:
        return t2w_d[t]
    return t

def t_ID(t):
  r'[a-zA-Z_][a-zA-Z_0-9]*'
  return t


t_CORK = r'\:\-'
t_DELIM = r'\.'
t_AND = r'\,'
t_OR = r'\;'
t_OBR = r'\('
t_CBR = r'\)'

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
  print("Illegal character '%s' at line %i pos %i." % (t.value, t.lineno, t.lexpos - update_lex_pos.pos_subst))
  t.lexer.skip(1)
  raise ValueError("")
  tokenize_file.no_errs = False


def tokenize_file(file_name):
  update_lex_pos.prev_tok_pos = 0
  update_lex_pos.pos_subst = 0
  update_lex_pos.prev_line = 1

  lexer = lex.lex()
  tokens = []
  tokenize_file.no_errs = True

  with open(file_name, 'r') as inf:
    lexer.input(inf.read())

  while True:
    tok = lexer.token()
    if not tok:
      break
    update_lex_pos(tok)
    tok.lexpos -= update_lex_pos.pos_subst
    tokens.append(tok)
    #print(', '.join(list(map(str,[tok.type, tok.value, tok.lineno, tok.lexpos]))))

  #print(tokens, tokenize_file.no_errs)
  return tokenize_file.no_errs, tokens


lexer = lex.lex()

#tokenize_file(sys.argv[1])