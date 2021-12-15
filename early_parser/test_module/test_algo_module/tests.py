from unittest import TestCase
from random import randint
from early_parser.algo import *


class AlgoTests(TestCase):
    def is_psp(self, s: str) -> bool:
        q = []
        for c in s:
            if c == 'a':
                q.append(c)
            else:
                if len(q) == 0 or q[0] != 'a':
                    return False
                q.pop()
        return len(q) == 0

    def test_init(self):
        solver = Algo()
        for it in range(100):
            l = 1 + randint(0, 100)
            s = str()
            for i in range(l):
                s = s + chr(ord('a') + randint(0, 2))
            self.assertFalse(solver.has_word(s))


