from unittest import TestCase

from early_parser.grammar import *


class GrammarTests(TestCase):
    def test_parse_rules(self):
        q = parse_rules("F->1|tht |tRt")
        self.assertEqual(len(q), 3)
        self.assertEqual(q, ['F->', 'F->tht', 'F->tRt'])
        self.assertEqual(['F->'], parse_rules("F->1"))

    def test_non_terminal(self):
        self.assertTrue(is_non_terminal('A'))
        self.assertFalse(is_non_terminal('2'))
        self.assertFalse(is_non_terminal('v'))
        self.assertTrue(is_non_terminal('F'))

    def test_single_rule(self):
        self.assertFalse(is_valid_single_rule("dfsd"))
        self.assertFalse(is_valid_single_rule("Adfsg"))
        self.assertFalse(is_valid_single_rule("a->Adfsg"))
        self.assertTrue(is_valid_single_rule("D->"))
        self.assertTrue(is_valid_single_rule("R->Adfsg"))
        self.assertTrue(is_valid_single_rule("A->1"))
        self.assertFalse(is_valid_single_rule("A->1sdf"))
        self.assertFalse(is_valid_single_rule("A-dsfs"))
        self.assertFalse(is_valid_single_rule("A->34fdgf"))
        self.assertFalse(is_valid_single_rule("A->1|dsf"))
        self.assertTrue(is_valid_single_rule("A->sdfsaaFDs"))

    def test_multi_rules(self):
        self.assertTrue(is_valid_rule("A->||"))
        self.assertTrue(is_valid_rule("A->1|edfslr|1"))
        self.assertFalse(is_valid_rule("a->dsfs"))
        self.assertTrue(is_valid_rule("A->sdS|fl|1"))
        self.assertFalse(is_valid_rule("A->43|t"))
        self.assertFalse(is_valid_rule("A->sdfsdDaS|pf2"))
        self.assertTrue(is_valid_rule("F->1|feFkjdg|ds"))

    def test_start(self):
        g = Grammar('I')
        self.assertEqual(g.get_start(), 'I')
        k = Grammar()
        self.assertEqual(k.get_start(), 'S')

    def test_add_rules(self):
        g = Grammar()
        self.assertFalse(g.add_rule("asdf"))
        self.assertEqual(len(g), 0)
        self.assertTrue(g.add_rule("T->1"))
        self.assertEqual(len(g), 1)
        self.assertTrue(g.add_rule("T->1|asd|afdasR"))
        self.assertEqual(len(g), 4)

    def test_similar_rules(self):
        g = Grammar()
        g.add_rule("T->f|asd|fsdg")
        self.assertEqual(len(g), 3)
        g.add_rule("T->f")
        self.assertEqual(len(g), 4)
        g.del_similar_rules()
        self.assertEqual(len(g), 3)
        for i in range(100):
            g.add_rule("T->gfd")
        g.del_similar_rules()
        self.assertEqual(len(g), 4)

    def test_erase(self):
        g = Grammar()
        g.add_rule("T->f|asd|fsdg")
        t = g.__iter__()
        self.assertEqual(t.__next__(), 'T->f')
        g.erase_rule(t)
        self.assertEqual(len(g), 2)
        t = g.__iter__()
        self.assertEqual(g.erase_rule(t), t)

    def test_size(self):
        g = Grammar()
        g.add_rule("T->k")
        self.assertEqual(g.__len__('T'), 1)
        self.assertEqual(g.__len__(), 1)
        self.assertEqual(g.__len__('a'), 0)
