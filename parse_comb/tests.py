from parsita import Success, Failure

from combinators import PrologParser


def test_module_dec():
    parse_fn = PrologParser.module_decl.parse
    assert type(parse_fn('module example.')) == Success
    assert type(parse_fn('module eXAmPle.')) == Success
    assert type(parse_fn('module f.')) == Success

    assert type(parse_fn('Module example.')) == Failure
    assert type(parse_fn('modul example.')) == Failure
    assert type(parse_fn('module example')) == Failure
    assert type(parse_fn('module Example.')) == Failure
    assert type(parse_fn('module.')) == Failure
    assert type(parse_fn('.')) == Failure


def test_atom():
    parse_fn = PrologParser.atom.parse
    assert type(parse_fn('a b')) == Success
    assert type(parse_fn('a b C')) == Success
    assert type(parse_fn('a B')) == Success
    assert type(parse_fn('a (b C)')) == Success
    assert type(parse_fn('a q b')) == Success
    assert type(parse_fn('a (q) b')) == Success
    assert type(parse_fn('a (b C) d e f')) == Success
    assert type(parse_fn('a (b C) D E F')) == Success
    assert type(parse_fn('a (b C) d E f')) == Success
    assert type(parse_fn('a (b C) d E f')) == Success
    assert type(parse_fn('a (b C) (((d E))) f')) == Success
    assert type(parse_fn('a (b (c))')) == Success
    assert type(parse_fn('a ((A)) b')) == Success

    assert type(parse_fn('type b')) == Failure
    assert type(parse_fn('a module')) == Failure
    assert type(parse_fn('A b')) == Failure
    assert type(parse_fn('A B')) == Failure
    assert type(parse_fn('a ((b) c)')) == Failure
    assert type(parse_fn('a (((b c))')) == Failure
    assert type(parse_fn('a (((b (((c)) d e f))))')) == Failure
    assert type(parse_fn('a b ()')) == Failure
    assert type(parse_fn('a (B c)')) == Failure
    assert type(parse_fn('a ((A) b)')) == Failure

def test_type_dec():
    parse_fn = PrologParser.type_decl.parse
    assert type(parse_fn('type fruit string -> string -> string -> o.')) == Success
    assert type(parse_fn('type filter (A -> o) -> o.')) == Success
    assert type(parse_fn('type filter t.')) == Success
    assert type(parse_fn('type filter (A -> o) -> list A -> list A -> o.')) == Success
    assert type(parse_fn('type filter string -> list A.')) == Success
    assert type(parse_fn('type filter (A -> (B -> C -> (A -> list A) -> C)) -> o.')) == Success
    assert type(parse_fn('type filter ((A -> (B -> C -> (A -> list A) -> C))) -> o.')) == Success
    assert type(parse_fn('type filter (A -> (B -> C -> (A -> (list A)) -> C)) -> o.')) == Success
    assert type(parse_fn('type filter (A -> (B -> C -> (A -> list A) -> (i am atom))) -> o.')) == Success
    assert type(parse_fn('type filter (A -> (B -> C -> (A -> list A) -> i am atom)) -> o.')) == Success

    assert type(parse_fn('type.')) == Failure
    assert type(parse_fn('type -> x.')) == Failure
    assert type(parse_fn('type type type -> type.')) == Failure
    assert type(parse_fn('type x -> y -> z.')) == Failure
    assert type(parse_fn('tupe x o.')) == Failure
    assert type(parse_fn('type filter (A -> (B -> C -> (A -> list A) -> C)) -> o')) == Failure


def test_lists():
    parse_fn = PrologParser.list_comb.parse
    parse_fn2 = PrologParser.atom.parse
    assert type(parse_fn('[]')) == Success
    assert type(parse_fn('[[]]')) == Success
    assert type(parse_fn('[[], [[]]]')) == Success
    assert type(parse_fn('[X, Y, Z]')) == Success
    assert type(parse_fn('[a (b c), d, Z]')) == Success
    assert type(parse_fn('[H | T]')) == Success
    assert type(parse_fn('[a (b c) | T]')) == Success
    assert type(parse_fn('[[X, [H | T]] | Z]')) == Success
    assert type(parse_fn('[[a], [b, c]]')) == Success
    assert type(parse_fn('[[X, [H | T]], x | Z]')) == Success
    assert type(parse_fn('[a, b, Z, [x, y | Z], [X, [H | T]], x | Z]')) == Success
    assert type(parse_fn2('g [X] Y')) == Success


    assert type(parse_fn('[')) == Failure
    assert type(parse_fn(']a, b, c[')) == Failure
    assert type(parse_fn('[H | abc]')) == Failure
    assert type(parse_fn('[H | A b c]')) == Failure
    assert type(parse_fn2('[X] Y')) == Failure
    assert type(parse_fn('[X, Y, Z, ]')) == Failure
    assert type(parse_fn('[| Z]')) == Failure

def test_rel():
    parse_fn = PrologParser.rel_decl.parse
    assert type(parse_fn('f.')) == Success
    assert type(parse_fn('f :- g.')) == Success
    assert type(parse_fn('f :- g, h; t.')) == Success
    assert type(parse_fn('f :- g, (h; t).')) == Success
    assert type(parse_fn('f a :- g, h (t c d).')) == Success
    assert type(parse_fn('f (cons h t) :- g h, f t.')) == Success
    assert type(parse_fn('g [X] Y :- f X Y.')) == Success
    assert type(parse_fn('g [X] Y :- f [X|Y] ; (x y , z).')) == Success
    assert type(parse_fn('g [X] Y :- f [X|Y] ; (x [] , z).')) == Success

    assert type(parse_fn('f')) == Failure
    assert type(parse_fn(':- f.')) == Failure
    assert type(parse_fn('f :- .')) == Failure
    assert type(parse_fn('f :- g; h, .')) == Failure
    assert type(parse_fn('f :- (g; (f).')) == Failure
    assert type(parse_fn('f ().')) == Failure
    assert type(parse_fn('[X] Y :- f X Y.')) == Failure


def test_program():
    parse_fn = PrologParser.program.parse
    assert type(parse_fn('module test.')) == Success
    assert type(parse_fn('module test. type t f -> o.')) == Success
    assert type(parse_fn('module test. type t f -> o. type t f -> o.')) == Success
    assert type(parse_fn('module test. type t f -> o. type t f -> o. f :- name.')) == Success
    assert type(parse_fn('module test. type t f -> o. type t f -> o. f :- name. a (b c) :- x, y, z.')) == Success
    assert type(parse_fn('type t f -> o. type t f -> o. f :- name. a (b c) :- x, y, z.')) == Success
    assert type(parse_fn('type t f -> o. f :- name. a (b c) :- x, y, z.')) == Success
    assert type(parse_fn('f :- name. a (b c) :- x, y, z.')) == Success
    assert type(parse_fn('a (b c) :- x, y, z.')) == Success

    assert type(parse_fn('\\ .')) == Failure
    assert type(parse_fn('% * .')) == Failure
    assert type(parse_fn('module test. module test2. type t f -> o. type t f -> o. f :- name. a (b c) :- x, y, z.')) == Failure
    assert type(parse_fn('module test. type t f -> o. type t f -> o. f :- name. a (b c) :- x, y, z. type x y')) == Failure
    assert type(parse_fn('type t f -> o. type t f -> o. f :- name. a (b c) :- x, y, z. module test.')) == Failure
    assert type(parse_fn('module test. type t f -> o.. type t f -> o. f :- name. a (b c) :- x, y, z.')) == Failure
    assert type(parse_fn('module test. type t f -> o. type t f -> o. f :- name. a (b c) -> x, y, z.')) == Failure
    assert type(parse_fn('module test. type t f -> o. type t f -> o f :- name. a (b c) :- x, y, z.')) == Failure
    assert type(parse_fn('module test. type t f -> o. (type t f -> o.) f :- name. a (b c) :- x, y, z.')) == Failure


def test_file(file_name, res):
    with open(file_name, 'r') as inf:
        assert type(PrologParser.program.parse(inf.read())) == res


def outer_tests():
    assert type(PrologParser.identif.parse("abc")) == Success
    assert type(PrologParser.identif.parse("aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPrRsStTuUvVwWxXyYzZ_1234567890")) == Success

    assert type(PrologParser.identif.parse("123abc")) == Failure
    assert type(PrologParser.identif.parse("Xyz")) == Failure

    assert type(PrologParser.var.parse("Abc")) == Success
    assert type(PrologParser.var.parse("H")) == Success

    assert type(PrologParser.var.parse("123abc")) == Failure
    assert type(PrologParser.var.parse("xyz")) == Failure

    assert type(PrologParser.atom.parse("a")) == Success
    assert type(PrologParser.atom.parse("a b c")) == Success
    assert type(PrologParser.atom.parse("a (b c)")) == Success
    assert type(PrologParser.atom.parse("a ((b c))")) == Success
    assert type(PrologParser.atom.parse("a ((b c)) d")) == Success
    assert type(PrologParser.atom.parse("a ((b c))  (d)")) == Success
    assert type(PrologParser.atom.parse("a ((b  c))  (d)")) == Success
    assert type(PrologParser.atom.parse("a ((b  c) )  ( d )")) == Success
    assert type(PrologParser.atom.parse("a((b c))(d)")) == Success

    assert type(PrologParser.atom.parse("a (a")) == Failure
    assert type(PrologParser.atom.parse("X a")) == Failure
    assert type(PrologParser.atom.parse("(a)")) == Failure

    assert type(PrologParser.rel_decl.parse("a.")) == Success
    assert type(PrologParser.rel_decl.parse("a b.")) == Success
    assert type(PrologParser.rel_decl.parse("a:-a.")) == Success
    assert type(PrologParser.rel_decl.parse("a:-a b.")) == Success
    assert type(PrologParser.rel_decl.parse("a b:- (a b)  .")) == Success
    assert type(PrologParser.rel_decl.parse("a b:- a;b,c.")) == Success
    assert type(PrologParser.rel_decl.parse("a b:- a;(b,c).")) == Success
    assert type(PrologParser.rel_decl.parse("a b:- (a;b),c.")) == Success
    assert type(PrologParser.rel_decl.parse("a b:- a;b;c.")) == Success
    assert type(PrologParser.rel_decl.parse("a b:- a,b,c.")) == Success
    assert type(PrologParser.rel_decl.parse("a (b (c))  :- (a b) .")) == Success

    assert type(PrologParser.type_seq.parse("a")) == Success
    assert type(PrologParser.type_seq.parse("Y -> X")) == Success

    assert type(PrologParser.type_decl.parse("type a b.")) == Success
    assert type(PrologParser.type_decl.parse("type a b -> X.")) == Success
    assert type(PrologParser.type_decl.parse("type filter (A -> o) -> list a -> list a -> o.")) == Success
    assert type(PrologParser.type_decl.parse("type filter (A -> o) -> list A -> list A -> o.")) == Success


if __name__ == '__main__':
    test_module_dec()
    test_atom()
    test_type_dec()
    test_lists()
    test_rel()
    test_program()
    test_file('../prolog/test.plg', Success)
    test_file('../prolog/auto.plg', Success)
    test_file('../prolog/test2.plg', Success)
    outer_tests()
    print('All tests passed')