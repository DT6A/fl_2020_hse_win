from enum import Enum


class RegexpType(Enum):
    EMPTY = 0
    EPSILON = 1
    CHAR = 2
    SEQ = 3
    ALT = 4
    STAR = 5


unnullable_l = [RegexpType.EMPTY, RegexpType.CHAR]
nullable_l = [RegexpType.EPSILON, RegexpType.STAR]


class Regexp:
    def __init__(self, regexp_type, p=None, q=None):
        if type(regexp_type) != RegexpType:
            raise ValueError('Wrong type for regexp')
        self.type = regexp_type
        self.p = p
        self.q = q

    def nullable(self):
        if self.type in nullable_l:
            return True
        elif self.type in unnullable_l:
            return False
        else:
            p_nullable = self.p.nullable()
            q_nullable = self.q.nullable()
            return p_nullable and q_nullable if self.type == RegexpType.SEQ else p_nullable or q_nullable

    def derivative(self, char):
        if self.type == RegexpType.EMPTY or self.type == RegexpType.EPSILON:
            return Regexp(RegexpType.EMPTY)
        elif self.type == RegexpType.CHAR:
            return Regexp(RegexpType.EPSILON) if self.p == char else Regexp(RegexpType.EMPTY)
        elif self.type == RegexpType.ALT:
            return Regexp(RegexpType.ALT, self.p.derivative(char), self.q.derivative(char))
        elif self.type == RegexpType.SEQ:
            if self.p.nullable():
                return Regexp(
                    RegexpType.ALT,
                    Regexp(RegexpType.SEQ, self.p.derivative(char), self.q), self.q.derivative(char)
                )
            else:
                return Regexp(RegexpType.SEQ, self.p.derivative(char), self.q)
        else:
            return Regexp(RegexpType.SEQ, self.p.derivative(char), Regexp(RegexpType.STAR, self.p))

    def match(self, s):
        r = self
        for c in s:
            r = r.derivative(c)
        return r.nullable()


class Empty(Regexp):
    def __init__(self):
        super(Empty, self).__init__(RegexpType.EMPTY)


class Epsilon(Regexp):
    def __init__(self):
        super(Epsilon, self).__init__(RegexpType.EPSILON)


class Char(Regexp):
    def __init__(self, char):
        super(Char, self).__init__(RegexpType.CHAR, char)


def Seq(r, q):
    if r.type == RegexpType.EMPTY or q.type == RegexpType.EMPTY:
        return Empty()
    elif r.type == RegexpType.EPSILON:
        return q
    elif q.type == RegexpType.EPSILON:
        return r
    else:
        return Regexp(RegexpType.SEQ, r, q)


def comp_regs(p, q):
    if p == None and q == None:
        return True
    if type(p) != type(q):
        return False

    if type(p) == str:
        return p == q
    elif p.type == q.type:
        lv = comp_regs(p.p, q.p)
        if not lv:
            return False
        rv = comp_regs(p.q, q.q)
        return rv
    else:
        return False


def Alt(r, q):
    if r.type == RegexpType.EMPTY:
        return q
    elif q.type == RegexpType.EMPTY:
        return r
    elif r.type == RegexpType.EPSILON:
        return q if q.nullable() else Regexp(RegexpType.ALT, Epsilon(), q)
    elif q.type == RegexpType.EPSILON:
        return r if r.nullable() else Regexp(RegexpType.ALT, Epsilon(), r)
    elif comp_regs(r, q):
        return r
    else:
        return Regexp(RegexpType.ALT, r, q)


def Star(r):
    if r.type == RegexpType.EMPTY or r.type == RegexpType.EPSILON:
        return Epsilon()
    elif r.type == RegexpType.STAR:
        return r
    else:
        return Regexp(RegexpType.STAR, r)
