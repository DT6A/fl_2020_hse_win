from parsita import *

class PrologParser(TextParsers, whitespace=r'[ \t\n\r]*'):
    kw_module = lit('module') > (lambda x: '(MODULE ')
    kw_type = lit('type') > (lambda x: '(TYPE ')

    dot = lit('.') > (lambda x: '')
    arrow = lit('->') > (lambda x: '')
    list_sep = lit(',')
    list_ht = lit('|') > (lambda x: '')
    cork = lit(':-') > (lambda x: '')
    disj_s = lit(';') > (lambda x: '')
    conj_s = lit(',') > (lambda x: '')
    obr = lit('(') > (lambda x: '')
    cbr = lit(')') > (lambda x: '')
    lob = lit('[') > (lambda x: '')
    lcb = lit(']') > (lambda x: '')

    lcword = reg(r'[a-z_][a-zA-Z_0-9]*')
    var = reg(r'[A-Z][a-zA-Z_0-9]*') > (lambda x: '(VAR ' + x + ')')
    identif = pred(lcword, lambda x: x != 'type' and x != 'module', 'identifier which is not a keyword') > (lambda x : '(ID ' + x + ')')

    #list_comb = fwd()

    #atom_proxy = fwd()
    #atom_proxy2 = fwd()
    l_atm1 = lambda x: ''.join(list(map(lambda y: str(y) if y != [] else '', x)))
    l_atm2 = lambda x: '(ATOM ' + ''.join(list(map(lambda y: str(y) if y != [] else '', x))) + ')'
    l_atm3 = lambda x: ''.join(list(map(lambda y: str(y) if y != [] else '', x)))
    atom = (identif & (rep(atom_proxy| atom_proxy2) > l_atm1)) > l_atm2
    atom_proxy = (atom | obr & atom_proxy & cbr) > l_atm3
    atom_proxy2 = (atom | (var | identif | list_comb) & (rep(atom_proxy2) > l_atm1)) > l_atm3

    #type_comb = fwd()
    #type_comb2 = fwd()
    type_seq = rep1sep(type_comb, arrow) > (lambda x: '(TYPESEQ ' + ''.join(x) + ')')
    type_comb = atom | var | obr & type_comb2 & cbr > (lambda x: ''.join(x))
    type_comb2 = ((atom | var | obr & type_seq & cbr) & arrow & type_seq) > (lambda x: '(TYPESEQ ' + ''.join(x) + ')')

    l_list = (lambda x: '[LIST ' + ''.join(x) + ']')
    list_comb = (lob & ((((atom | var | list_comb) & list_ht & var) > l_list) | (repsep(atom | var | list_comb, list_sep) > l_list)) & lcb) > l_atm1


    expr = obr & disj & cbr | atom
    conj = ((expr & conj_s & conj > (lambda x: '(AND ' + ''.join(x) + ')'))  | expr > (lambda x: ''.join(x)))
    disj = ((conj & disj_s & disj > (lambda x: '(OR ' + ''.join(x) + ')')) | conj > (lambda x: ''.join(x)))

    module_decl = kw_module & identif & dot > (lambda x: ''.join(x) + ')')
    type_decl = kw_type & identif & type_seq & dot > (lambda x: ''.join(x) + ')')
    rel_decl = (((atom & cork & disj) > (lambda x: '(HEAD ' + x[0] + ')(BODY ' + x[2] +')') )| atom) & dot > (lambda x: '(REL ' + x[0] + ')')

    program = ((module_decl) & (rep(type_decl) > (lambda x: '\n'.join(x))) & (rep(rel_decl) > (lambda x: '\n'.join(x)))) > (lambda x: '\n'.join(x))


if __name__ == '__main__':
    '''
    print(PrologParser.module_decl.parse('module    example.\t'))

    print(PrologParser.atom.parse('a b'))
    print(PrologParser.atom.parse('A b'))
    print(PrologParser.atom.parse('A B'))
    print(PrologParser.atom.parse('a b C'))
    print(PrologParser.atom.parse('a B'))
    print(PrologParser.atom.parse('a (B c)'))
    print(PrologParser.atom.parse('a (b C)'))
    print(PrologParser.atom.parse('a (b C) d e f'))
    print(PrologParser.atom.parse('a (b C) D E F'))
    print(PrologParser.atom.parse('a (b C) d E f'))
    
    print(PrologParser.type_decl.parse('type fruit string -> string -> string -> o.'))
    print(PrologParser.type_decl.parse('type filter (A -> o) -> o.'))
    print(PrologParser.type_decl.parse('type filter t.'))
    print(PrologParser.type_decl.parse('type filter (A -> o) -> list A -> list A -> o.'))
    print(PrologParser.type_decl.parse('type filter string -> list A.'))
    print(PrologParser.type_decl.parse('type type type -> type.'))
    print(PrologParser.type_decl.parse('type x -> y -> z.'))
    print(PrologParser.type_decl.parse('tupe x o.'))
    print(PrologParser.type_decl.parse('type filter (A -> (B -> C -> (A -> list A) -> C)) -> o.'))
    print(PrologParser.type_decl.parse('type filter ((A -> (B -> C -> (A -> list A) -> C))) -> o.'))
    print(PrologParser.type_decl.parse('type filter (A -> (B -> C -> (A -> (list A)) -> C)) -> o.'))
    print(PrologParser.type_decl.parse('type filter (A -> (B -> C -> (A -> list A) -> (C))) -> o.'))

    print(PrologParser.list_comb.parse('[]'))
    print(PrologParser.list_comb.parse('[X, Y, Z]'))
    print(PrologParser.list_comb.parse('[a (b c), d, Z]'))
    print(PrologParser.list_comb.parse('['))
    print(PrologParser.list_comb.parse(']a, b, c['))
    print(PrologParser.list_comb.parse('[H | T]'))
    print(PrologParser.list_comb.parse('[a (b c) | T]'))
    print(PrologParser.list_comb.parse('[H | abc]'))
    print(PrologParser.list_comb.parse('[H | A b c]'))
    print(PrologParser.list_comb.parse('[[X, [H | T]] | Z]'))
    print(PrologParser.list_comb.parse('[[a], [b, c]]'))
    print(PrologParser.atom.parse('[X] Y'))
    print(PrologParser.atom.parse('g [X] Y'))

    print(PrologParser.rel_decl.parse('f.'))
    print(PrologParser.rel_decl.parse('f :- g.'))
    print(PrologParser.rel_decl.parse('f :- g, h; t.'))
    print(PrologParser.rel_decl.parse('f :- g, (h; t).'))
    print(PrologParser.rel_decl.parse('f a :- g, h (t c d).'))
    print(PrologParser.rel_decl.parse('f (cons h t) :- g h, f t.'))
    print(PrologParser.rel_decl.parse('g [X] Y :- f X Y.'))
    print(PrologParser.rel_decl.parse('[X] Y :- f X Y.'))
    print(PrologParser.rel_decl.parse('f'))
    print(PrologParser.rel_decl.parse(':- f.'))
    print(PrologParser.rel_decl.parse('f :- .'))
    print(PrologParser.rel_decl.parse('f :- g; h, .'))
    print(PrologParser.rel_decl.parse('f :- (g; (f).'))
    print(PrologParser.rel_decl.parse('f ().'))

    print(PrologParser.rel_decl.parse('a b c.'))
    print(PrologParser.rel_decl.parse('a (b c).'))
    print(PrologParser.rel_decl.parse('a (a C).'))
    print(PrologParser.rel_decl.parse('a (b (c)).'))
    '''

    print(PrologParser.program.parse('module test. type t f -> o. type t f -> o. f :- kek. a (b c) :- x, y, z.').value)