import sys

from parsita import *

def foldl(f, l, v):
    res = v
    l = l[::-1]
    for i in l:
        res = f(i, res)
    return res

def process_list(l, v):
    res = l.rindex('nil')
    l = l[:res] + v + l[res + 3:]
    return l

class PrologParser(TextParsers, whitespace=r'[ \t\n\r]*'):
    kw_module = lit('module') > (lambda x: '(MODULE ')
    kw_type = lit('type') > (lambda x: '(TYPE ')

    l_skip = (lambda x: '')
    dot = lit('.') > l_skip
    arrow = lit('->') > l_skip
    list_sep = lit(',')
    list_ht = lit('|') > l_skip
    cork = lit(':-') > l_skip
    disj_s = lit(';') > l_skip
    conj_s = lit(',') > l_skip
    obr = lit('(') > l_skip
    cbr = lit(')') > l_skip
    lob = lit('[') > l_skip
    lcb = lit(']') > l_skip

    lcword = reg(r'[a-z_][a-zA-Z_0-9]*')
    var = reg(r'[A-Z][a-zA-Z_0-9]*') > (lambda x: '(VAR ' + x + ')')
    identif = pred(lcword, lambda x: x != 'type' and x != 'module', 'identifier which is not a keyword') > (lambda x : '(ID ' + x + ')')

    l_atm1 = lambda x: ''.join(list(map(lambda y: str(y) if y != [] else '', x)))
    l_atm2 = lambda x: '(ATOM ' + ''.join(list(map(lambda y: str(y) if y != [] else '', x))) + ')'
    l_atm3 = lambda x: ''.join(list(map(lambda y: str(y) if y != [] else '', x)))

    atom = (identif & (rep(((obr & atom_proxy & cbr) > (lambda x: x[1])) | atom_proxy2) > l_atm1)) > l_atm2
    atom_proxy = ((atom > (lambda x: '(' + x + ')')) | obr & (atom_proxy | var) & cbr) > l_atm1
    atom_proxy2 = (atom | (var | identif | list_comb) & (rep(atom_proxy2) > l_atm1)) > l_atm3

    type_seq = rep1sep(type_comb, arrow) > (lambda x: '(TYPESEQ ' + ''.join(x) + ')')
    type_comb = atom | var | obr & type_seq & cbr > (lambda x: ''.join(x))
    #type_comb2 = ((atom | var | obr & type_seq & cbr) & arrow & type_seq) > (lambda x: '(TYPESEQ ' + ''.join(x) + ')')

    l_list = (lambda x: foldl(lambda y, z: '(cons ' + y + ' ' + z + ')', x, 'nil'))
    l_short_list = (lambda x: '(cons (' + x[0] + ')' + x[2] + ')')
    l_compl_list = (lambda x: process_list(x[0], x[2]))
    list_coma = repsep(atom | var | list_comb, list_sep) > l_list
    list_comb = (lob & ((((atom | var | list_comb) & list_ht & var) > l_short_list) | ((list_coma & list_ht & var)  > l_compl_list) | list_coma) & lcb) > l_atm1

    expr = (obr & disj & cbr | atom) > (lambda x: ''.join(x))
    conj = ((expr & conj_s & conj > (lambda x: '(AND ' + ''.join(x) + ')'))  | expr)
    disj = ((conj & disj_s & disj > (lambda x: '(OR ' + ''.join(x) + ')')) | conj > (lambda x: ''.join(x)))

    module_decl = opt(kw_module & identif & dot) > (lambda x: ''.join(x[0]) + ')' if len(x) > 0 else '')
    type_decl = kw_type & identif & type_seq & dot > (lambda x: ''.join(x) + ')')
    rel_decl = (((atom & cork & disj) > (lambda x: '(HEAD ' + x[0] + ')(BODY ' + x[2] +')') )| atom) & dot > (lambda x: '(REL ' + x[0] + ')')

    l_nl = (lambda x: '\n'.join(x))
    program = ((module_decl) & (rep(type_decl) > l_nl) & (rep(rel_decl) > l_nl)) > l_nl


if __name__ == '__main__':
    s2p = {
        '--atom': PrologParser.atom.parse,
        '--typeexpr': PrologParser.type_seq.parse,
        '--type': PrologParser.type_decl.parse,
        '--module': PrologParser.module_decl.parse,
        '--relation': PrologParser.rel_decl.parse,
        '--list': PrologParser.list_comb.parse,
        '--prog': PrologParser.program.parse,
    }
    sys.stdout = open(sys.argv[2] + '.out', 'w')
    with open(sys.argv[2], 'r') as inf:
        result = s2p[sys.argv[1]](inf.read())
        if type(result) == Success:
            print(result.value)
        else:
            print(result.message)