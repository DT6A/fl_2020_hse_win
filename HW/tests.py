import time
import sys

from regexp import *

sys.setrecursionlimit(10000)


def profile_test(re, s, re_s, ca=None):
    start_time = time.time()
    res = re.match(s)
    if ca is not None:
        assert ca == res
    elapsed_time = time.time() - start_time
    print("Time: %3.7f" % elapsed_time, "String len: %6i" % len(s), "RE:", re_s)


a = Char('a')

b = Char('b')

c = Char('c')

# \epsilon
r0 = Epsilon()

# a*a
r1 = Seq(Star(a), a)

# (a|a)*
r2 = Star(Alt(a, a))

# b | (c (a|b)*)
r3 = Alt(b, Seq(c, Star(Alt(a, b))))

# (a|a)*a(a|a)*
r4 = Seq(Seq(Star(Alt(a, a)), a), Star(Alt(a, a)))

# (a|b)*(a|b)
r5 = Seq(Star(Alt(a, b)), Alt(a, b))

# (a|b)*(a|b)(a|b)*
r6 = Seq(Seq(Star(Alt(a, b)), Alt(a, b)), Star(Alt(a, b)))

# a*
r7 = Star(a)

# (a|b)*
r8 = Star(Alt(a, b))

# (a|b|c)*
r9 = Star(Alt(a, Alt(b, c)))

# a?
r10 = Alt(a, Epsilon())

# (ab)*
r11 = Star(Seq(a, b))

# (abc)*
r12 = Star(Seq(Seq(a, b), c))

print("Correctness tests")
profile_test(r0, '', '\epsilon', True)
profile_test(r0, 'a', '\epsilon', False)

profile_test(r1, 'a' * 250, 'a*a', True)
profile_test(r1, 'a' * 250 + 'b', 'a*a', False)

profile_test(r2, 'a' * 50, '(a|a)*', True)
profile_test(r2, 'a' * 50 + 'b', '(a|a)*', False)

profile_test(r10, '', 'a?', True)
profile_test(r10, 'a', 'a?', True)
profile_test(r10, 'b', 'a?', False)

s_list = ["b", "c", "d", "ba", "aaaa", "c" + "abba" * 25, "c" + "abba" * 50, "c" + "abba" * 100]
for s in s_list:
    profile_test(r3, s, 'b | (c (a|b)*)')

profile_test(r3, "cabba", 'b | (c (a|b)*)', True)
profile_test(r3, "cabba" * 625, 'b | (c (a|b)*)', False)

profile_test(r4, 'a' * 50, '(a|a)*a(a|a)*', True)
profile_test(r4, 'a' * 50 + 'b', '(a|a)*a(a|a)*', False)
profile_test(r4, 'a', '(a|a)*a(a|a)*', True)
profile_test(r4, '', '(a|a)*a(a|a)*', False)

print('\nComplexity length dependency')
for sl in range(25, 151, 25):
    profile_test(r1, 'a' * sl, 'a*a', True)
    profile_test(r4, 'a' * sl, '(a|a)*a(a|a)*', True)

print('\nComplexity length dependency 2')
for sl in range(25, 76, 25):
    profile_test(r5, 'ab' * sl, '(a|b)*(a|b)', True)
    profile_test(r6, 'ab' * sl, '(a|b)*(a|b)(a|b)*', True)

print('\nALT complexity dependency')
for sl in range(50, 151, 25):
    profile_test(r7, 'aa' * sl, 'a*', True)
    profile_test(r8, 'aa' * sl, '(a|b)*', True)
    profile_test(r9, 'aa' * sl, '(a|b|c)*', True)

print('\nSEQ complexity dependency')
for sl in range(25, 126, 25):
    profile_test(r7, 'a' * (sl * 3), 'a*', True)
    profile_test(r11, 'ab' * int(sl * 1.5), '(ab)*', True)
    profile_test(r12, 'abc' * sl, '(abc)*', True)