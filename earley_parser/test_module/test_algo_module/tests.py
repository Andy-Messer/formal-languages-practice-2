from random import randint
from unittest import TestCase

from early_parser.algo import *


def is_psp(s: str) -> bool:
    q = []
    for c in s:
        if c == 'a':
            q.append(c)
        else:
            if len(q) == 0 or q[0] != 'a':
                return False
            q.pop()
    return len(q) == 0


class AlgoTests(TestCase):

    def test_init(self):
        solver = Algo()
        for it in range(100):
            len_ = 1 + randint(0, 100)
            s = str()
            for i in range(len_):
                s = s + chr(ord('a') + randint(0, 2))
            self.assertFalse(solver.has_word(s))

    def test_simple(self):
        g = Grammar()
        g.add_rule("S->aSbS|")
        solver = Algo(g)
        self.assertTrue(solver.has_word('ab'))
        self.assertTrue(solver.has_word("abaabb"))
        self.assertFalse(solver.has_word("a"))
        s = str()
        for i in range(100):
            len_ = 1 + randint(0, 100)
            for j in range(len_):
                s = s + chr(ord('a') + randint(0, 2))
            self.assertEqual(solver.has_word(s), is_psp(s))

    def test_not_simple(self):
        g = Grammar()
        g.add_rule("S->SS|aSb|")
        solver = Algo(g)
        self.assertTrue(solver.has_word("ab"))
        self.assertTrue(solver.has_word("abaabb"))
        self.assertFalse(solver.has_word("a"))
        s = str()
        for i in range(100):
            len_ = 1 + randint(0, 100)
            for j in range(len_):
                s = s + chr(ord('a') + randint(0, 2))
            self.assertEqual(solver.has_word(s), is_psp(s))
