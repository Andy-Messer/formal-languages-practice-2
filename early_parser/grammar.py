# imports
import logging


#######################
# Section: Work with rules
#######################

def parse_rules(rule: str) -> list:
    """! Splits several rules written in one line into separate ones
    @param rule given rules
    @return rules list of split rules
    """
    logging.info(f"Parse %s by |", rule)
    start = rule[:3]
    logging.debug(f"splitting off th beginning")
    count = 0
    rules = []
    cur_rule = start
    for i in range(3, len(rule)):
        if rule[i] == '|':
            if len(cur_rule) == 4 and cur_rule[-1] == '1':
                cur_rule = cur_rule[:len(cur_rule) - 1]
            rules.append(cur_rule)
            count += 1
            logging.debug(f"New rule added!")
            cur_rule = start
        elif rule[i] == ' ':
            continue
        else:
            cur_rule += rule[i]
    if len(cur_rule) == 4 and cur_rule[-1] == '1':
        cur_rule = cur_rule[:len(cur_rule) - 1]
    rules.append(cur_rule)
    count += 1
    logging.debug(f"New rule added!")
    logging.info(f"Collected %d rules", count)
    for r in rules:
        logging.info(f"Collected rule %s", r)
    return rules


def is_valid_single_rule(rule: str) -> bool:
    """! Checks validity of a separate rule
    @param rule given rule
    return True if valid
    return False if not valid
    """
    logging.info(f"Check for validity %s", rule)
    valid = len(rule) >= 3 and is_non_terminal(rule[0]) and rule[1] == '-' and rule[2] == '>'
    if valid and len(rule) == 4 and rule[-1] == '1':
        logging.info(f"Validity of %s", True)
        return True
    for i in range(3, len(rule)):
        if not valid:
            break
        valid = is_symbol(rule[i]) or is_non_terminal(rule[i])
    logging.info(f"Validity of %s", valid)
    return valid


def is_valid_rule(rule: str) -> bool:
    logging.info(f"Check for validity %s", rule)
    valid = len(rule) > 3 and is_non_terminal(rule[0]) and rule[1] == '-' and rule[2] == '>'
    if not valid:
        logging.info(f"Validity of %s", False)
        return False
    single_rules = parse_rules(rule)
    for single_rule in single_rules:
        if not is_valid_single_rule(single_rule):
            logging.info(f"Validity of %s", False)
            return False
    logging.info(f"Validity of %s", True)
    return True


def is_non_terminal(c: str) -> bool:
    """! Checks the symbol for non-terminal
    @param c symbol
    @return: True is non-terminal
    @return: False is terminal
    """
    return 'A' <= c <= 'Z'


def is_symbol(c: str) -> bool:
    """! Checks belonging of the symbol to the alphabet
    @param c symbol
    @return: True is in alphabet
    @return: False not in the alphabet
    """
    return 'a' <= c <= 'z'


#######################
# Section: Work with Grammar
#######################

class Grammar:
    """! Realization of Context-free Grammar """
    _max_char_id = 26
    _size = int()
    _start = str()
    _rules = list()

    class _Iterator:
        """! Standard bidirectional Iterator for Grammar """
        char_id = int()
        rule_id = int()
        rules = list()
        _max_char_id = 26

        def get_rule(self):
            return self.rules[self.char_id][self.rule_id]

        def is_valid(self):
            return self._max_char_id > self.char_id >= 0 and \
                   0 <= self.rule_id < len(self.rules[self.char_id])

        def __init__(self, rules, c='A'):
            self.char_id = ord(c) - ord('A')
            self.rule_id = 0
            self.rules = rules

        def __iter__(self):
            return self

        def __next__(self):
            self.rule_id += 1
            if self.rule_id >= len(self.rules[self.char_id]):
                self.rule_id = 0
                self.char_id += 1
                while self.char_id < self._max_char_id and len(self.rules[self.char_id]) == 0:
                    self.char_id += 1
            if not self.is_valid():
                raise StopIteration
            return self.get_rule()

    def __init__(self, start: str = 'S'):
        logging.info(f"Initialize new grammar")
        self._start = start
        self._rules = [[] for _ in range(self._max_char_id)]
        self._size = 0
        self._iter = self.__iter__

    def get_start(self):
        return self._start

    # def input_init(self):
    #     """! Input the grammar from stdin """
    #     logging.info(f"Input grammar")
    #     self._size = int(input())
    #     for i in range(self._size):
    #         rule = input()
    #         self.add_rule(rule)

    def add_rule(self, rule: str) -> bool:
        """! Add rule to grammar
        @param rule given rule
        @return True correctly added
        @return False wasn't added
        """
        if is_valid_rule(rule):
            rules_pack = parse_rules(rule)
            for single_rule in rules_pack:
                self._rules[ord(single_rule[0]) - ord('A')].append(single_rule)
                self._size += 1
            logging.info(f"New rule added")
            return True
        logging.info(f"New rule wasn't added")
        return False

    def __len__(self, c: str = '') -> int:
        """!
        Outputs size of object
        @param c non-term
        @return size of container
        """
        if c == '':
            return self._size
        else:
            if is_non_terminal(c):
                return len(self._rules[ord(c) - ord('A')])
        return 0

    def del_similar_rules(self):
        """! Delete similar rules from grammar
        For this uses container - set
        """
        size = self._size
        self._size = 0
        single_rules = set()

        iterator = self._Iterator(self._rules)
        try:
            next(iterator)
            for i in range(size):
                single_rules.add(iterator.get_rule())
                next(iterator)
        except StopIteration:
            for i in range(self._max_char_id):
                self._rules[i] = []
            for rule in single_rules:
                self._rules[ord(rule[0]) - ord('A')].append(rule)
                self._size += 1
            logging.info(f"Similar rules deleted")

    def __iter__(self):
        self._iter = self._Iterator(self._rules)
        return self._iter.__iter__()

    # def __str__(self):
    #     """! This method allow to output grammar to stdout """
    #     sz = self._size
    #     output = str(sz) + '\n'
    #     iterator = self._Iterator(self._rules)
    #     for i in range(sz):
    #         if i + 1 != sz:
    #             output = output + next(iterator) + '\n'
    #         else:
    #             output = output + next(iterator)
    #     logging.info(f"dump grammar")
    #     return output

    # def __repr__(self):
    #     """! This method allow to convert grammar to string """
    #     output = str(self._size) + '\n'
    #     iterator = self._Iterator(self._rules)
    #     for i in range(self._size):
    #         if i + 1 != self._size:
    #             output = output + iterator.get_rule() + '\n'
    #         else:
    #             output = output + iterator.get_rule()
    #     logging.info(f"representing grammar")
    #     return output

    def erase_rule(self, it: _Iterator):
        """! Deleting rule by iterator
        @param it iterator
        @return iterator to the next element
        """
        if it.is_valid():
            nxt = self._Iterator(it.rules)
            nxt.char_id = it.char_id
            nxt.rule_id = it.rule_id
            next(nxt)
            logging.info(f"%s deleted", nxt.get_rule())
            self._rules[nxt.char_id].remove(nxt.get_rule())
            self._size -= 1
            return nxt
        return it
