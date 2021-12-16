##
# @file test_algo_module.py
#
# @brief A module - realization of Earley algorithm
#
# @section libraries_main Libraries/Modules
# - logging - module
# - grammar - Context-free grammar realization

# @section author Author(s)
# - Created by Andrey Krotov on 14/12/2021
# - Modified by Andrey Krotov on 14/12/2021
#
# Copyright (c) 2021 Andrey Krotov. All rights reserved.
from early_parser.grammar import *


class Algo:
    """! Realization of Earley algorithm """
    _grammar = None
    _levels = []

    def __init__(self, grammar: Grammar = Grammar()):
        self._grammar = grammar

    class _State:
        rule = str()
        rule_pos = int()
        str_pos = int()

        def __init__(self, rule: str, rule_pos: int, str_pos: int):
            logging.info(f"New state initialized")
            self.rule = rule
            hash(9)
            self.rule_pos = rule_pos
            self.str_pos = str_pos

        def __eq__(self, other):
            return self.rule == other.rule and self.rule_pos == other.rule_pos and self.str_pos == other.str_pos

        def __lt__(self, other):
            if self.rule_pos != other.rule_pos:
                return self.rule_pos < other.rule_pos
            if self.str_pos != other.str_pos:
                return self.str_pos < other.str_pos
            return self.rule < other.rule

        def __hash__(self):
            p = 13
            hash_ = self.str_pos
            hash_ += (self.rule_pos * (p**2)) % 567892342117
            k = 1
            for i in self.rule:
                hash_ += ord(i) * (p**(2 + k))
                k += 1
            return hash_

    def _scan(self, it: _State, level_id: int, c: str) -> bool:
        logging.info(f"_scan started level id:%d, string :%s", level_id, c)
        # зачем длины правил сравнивать
        if is_symbol(c) and len(it.rule) > it.rule_pos and it.rule[it.rule_pos] == c:
                prev_sz = len(self._levels[level_id + 1])
                self._levels[level_id + 1].add(self._State(it.rule, it.rule_pos + 1, it.str_pos))
                return len(self._levels[level_id + 1]) != prev_sz
        return False

    def _predict(self, _it: _State, level_id: int) -> bool:
        logging.info(f"_predict started level id:%d", level_id)
        if _it.rule_pos < len(_it.rule):
            if is_non_terminal(_it.rule[_it.rule_pos]):
                non_term = _it.rule[_it.rule_pos]
                # nxt_it вроде надо
                new_states = [self._State(it, 3, level_id) for it in self._grammar if it[0] == non_term]
                prev_sz = len(self._levels[level_id])
                for state in new_states:
                    self._levels[level_id].add(state)
                return len(self._levels[level_id]) != prev_sz
        return False

    def _complete(self, it: _State, level_id: int) -> bool:
        logging.info(f"_complete started level id:%d", level_id)
        if it.rule_pos == len(it.rule):
            non_terminal = it.rule[0]
            lvl = it.str_pos
            new_states = []
            for prev_it in self._levels[lvl]:
                if prev_it.rule_pos < len(prev_it.rule) and prev_it.rule[prev_it.rule_pos] == non_terminal:
                    new_states.append(self._State(prev_it.rule, prev_it.rule_pos + 1, prev_it.str_pos))
            prev_sz = len(self._levels[level_id])
            for new_state in new_states:
                self._levels[level_id].add(new_state)
            return len(self._levels[level_id]) != prev_sz
        return False

    def scan(self, _id: int, s: str):
        logging.info(f"main scan started")
        for it in self._levels[_id]:
            self._scan(it, _id, s[_id])

    def predict(self, _id: int) -> bool:
        logging.info(f"main predict started")
        changed = False
        its = [i for i in self._levels[_id]]
        for it in its:
            changed |= self._predict(it, _id)
        return changed

    def complete(self, _id: int) -> bool:
        logging.info(f"main complete started")
        changed = False
        its = [i for i in self._levels[_id]]
        for it in its:
            changed |= self._complete(it, _id)
        return changed

    def has_word(self, word: str) -> bool:
        """ Checks the presence of a word in the grammar
        @param word given word
        @return True if there is
        @return False if there isn't
        """
        self._levels = [set() for _ in range(len(word) + 1)]
        start_rule = '#->'
        start_rule += self._grammar.get_start()
        self._levels[0].add(self._State(start_rule, 3, 0))
        changed = True
        while changed:
            changed = self.complete(0)
            changed |= self.predict(0)
        for _id in range(len(word)):
            self.scan(_id, word)
            changed = True
            while changed:
                changed = self.complete(_id + 1)
                changed |= self.predict(_id + 1)
        result = self._State(start_rule, 4, 0)
        for state in self._levels[len(word)]:
            if state == result:
                return True
        return False
