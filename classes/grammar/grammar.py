from classes.grammar.edge import Edge
from classes.grammar.graph import Graph
from evaluate.timetest.average import average_timing_name, average_timing


class Grammar:
    def __init__(self, graph, terminal_func=None, rank_func=lambda x: 2, size_func=lambda x: 3, terminal_set=None):
        """Initializes a grammar object.
        :param graph: used as the start_rule of this grammar. start_rule has the name 0 implicitly. Should be a graph.
        :param terminal_func: decides, if a symbol is used as a terminal. (e.g. type == str --> terminal symbol)
        :param rank_func: calculates the rank of a terminal rule.
        :param size_func: calculates the size of a terminal rule."""

        self._rules = {0: graph}
        self._next_free_name = 1
        self.terminal_rank = rank_func
        self.terminal_size = size_func
        self._terminal_set = terminal_set
        self._terminal_func = terminal_func
        self._treat_as_terminal_rules = set()
        # the statements above are functional programming. it is possible now to invoke grammar.is_terminal(...)

    def __delitem__(self, key):
        """Deletes a rule with a given ID/Name.
        :param key: rule name to delete."""
        del self._rules[key]

    def __getitem__(self, item: int) -> Graph:
        """:returns a rule with a given ID/Name. Uses object[item]-Syntax"""
        return self._rules[item]

    def __setitem__(self, key, value):
        self._rules[key] = value

    def __len__(self):
        """:returns the number of Rules including the start_rule"""
        return len(self._rules)

    def __str__(self):
        """:returns a readable representation of this grammar object"""
        return self._rules.__str__()

    __repr__ = __str__  # both methods are the same now.

    def __iter__(self):
        """:returns an iterable over the rules within this grammar. Can be used by: for rule in grammar: ..."""
        return self._rules.__iter__()

    def __eq__(self, other):
        return self._rules == other._rules

    def get_start_rule_name(self):
        """:returns the start_rule_name: implicit it is id 0."""
        return 0

    def has_rule(self, rule_name):
        return rule_name in self._rules

    def is_terminal(self, symbol):
        if symbol in self._treat_as_terminal_rules:
            return True
        if self._terminal_set is not None:
            if symbol in self._terminal_set:
                return True
        if self._terminal_func is not None:
            if self._terminal_func(symbol):
                return True
        return False

    def get_unused_nonterminal(self):
        """:return the next ID not associated with a rule"""
        self._next_free_name += 1
        while self._next_free_name in self._rules or self.is_terminal(self._next_free_name):
            self._next_free_name += 1
        return self._next_free_name

    def rank_of_rule(self, rule_name):
        """:param rule_name: name of an existing rule.
        :returns the rank of the Rule with the given name.
        """
        if rule_name in self:
            return self[rule_name].rank()
        if self.is_terminal(rule_name):  # e.g. type(rule_name) is int:
            return self.terminal_rank(rule_name)
        else:
            raise ValueError(f'Rule name {rule_name} does not exists')

    def size_of_rule(self, rule_name):
        """:param rule_name: name of an existing rule.
        :returns the size of the Rule with the given name.
        """
        if self.is_terminal(rule_name):  # e.g. type(rule_name) is int:
            return self.terminal_size(rule_name)
        else:
            return self[rule_name].size_of()

    def size_of_hole_grammar(self):
        """:return the size of the while grammar"""
        return sum((self._rules[g].size_of() for g in self._rules.keys()))

    def add_rule(self, rule_name: int, rule: Graph):
        """Method used for adding a rule. Note that there is no check, if there is a rule with the given Name.
        :param rule_name: name of the new added rule.
        :param rule: the new added rule. Should be of type Graph."""
        self._rules[rule_name] = rule

    def delete_all_rules_except_start_rule(self):
        """Deletes all rules except the start rule. Only decompress uses this when the start rule is fully rebuild. """
        self._rules = {0: self._rules[0]}

    @average_timing
    def delete_all_mark_as_delete_edges(self):
        for rule in self._rules:
            for index in range(len(self[rule].get_edges())-1, -1, -1):  # go backwards, so no mix up with positions
                edge = self[rule][index]
                if edge.is_mark_as_delete() or edge.get_label() is None:
                    del self[rule][index]

    @average_timing
    def rename_rule(self, old_rule_name, new_rule_name):
        for rule in self._rules:
            for edge in self[rule].get_edges():  # go backwards, so no mix up with positions
                if edge.get_label == old_rule_name:
                    edge.change_label(new_rule_name)
        self.add_rule(new_rule_name, self[old_rule_name])
        del self[old_rule_name]

    def add_treat_as_terminal(self, symbol):
        self._treat_as_terminal_rules.add(symbol)

    def clear_treat_as_terminal(self):
        self._treat_as_terminal_rules.clear()

    # from now on, the functions are more complex

    @average_timing
    def merge(self, grammar):
        """Inline merge of a grammar into self. Extend of the start rule, insert of all other rules.
        Does not complete the operation CORRECTLY if a rule name already exists.
        :param grammar: other given grammar."""
        if self is grammar:
            return self
        print(f'merge {tuple(self._rules.keys())} and {tuple(grammar._rules.keys())}')
        for rule in grammar:
            if rule == 0:
                self[0].get_edges().extend(grammar[0].get_edges())
            elif self.has_rule(rule):
                self.rename_rule(rule, self.get_unused_nonterminal())
                self[rule] = grammar[rule]
            elif self.is_terminal(rule):
                raise ValueError(f'Not merge-able in this direction. Cannot change terminal {rule} to other name.')
            else:
                self[rule] = grammar[rule]
        old_terminal_rank = self.terminal_rank
        old_terminal_size = self.terminal_size

        def new_terminal_rank(label):
            try:
                value = old_terminal_rank(label)
                if value is None:
                    raise ValueError()
            except BaseException as e:
                value = grammar.terminal_rank(label)
            return value
        self.terminal_rank = new_terminal_rank

        def new_terminal_size(label):
            try:
                value = old_terminal_size(label)
                if value is None:
                    raise ValueError()
            except BaseException as e:
                value = grammar.terminal_size(label)
            return value
        self.terminal_size = new_terminal_size
        print(f'result {tuple(self._rules.keys())}')
        return self

    @average_timing
    def isolate_edge(self, label, path):
        """Isolates the edge the path is pointing towards begin at the rule with the given label.
        The edge is not removed."""
        if len(path) is 0:
            return
        elif len(path) is 1:
            return self[label].get_edges()[path[0].position]
        else:
            edge: Edge = self[path[-2].label].get_edges()[path[-1].position]
            path = path.add_before(-1, label)  # needed for last step. position is ignored
            for i in range(len(path)-2, 0, -1):
                hyperedge = self[path[i-1].label].get_edges()[path[i].position]
                edge = Edge(edge.get_label(), nodes=[hyperedge[node] for node in edge])
            return edge

    @average_timing_name('inline_rule_grammar')
    def inline_rule(self, label):
        """The rule with the name label will be inserted. That means, that each occurrence within the grammar will be
        replaced with the corresponding set of edges within the rule, that will be inserted. Nodes will be looked up
        accordingly.
        :param label: Name of the rule, that will be inserted.
        :returns Number of replacements"""

        if label is 0:
            raise ValueError('Start rule 0 cannot be inlined.')

        @average_timing_name('inline_create_edges')
        def get_edges_for_hyperedge(hyperedge):
            """Creates edges for the hyperedge corresponding to the given Rule.

            :param hyperedge: non-terminal of the rule given while this object is constructed.
            :returns the edges described by the given non-terminal.
            """
            try:
                return [Edge(e.get_label(), *[hyperedge[node] for node in e]) for e in rule_to_inline.get_edges()]
            except IndexError as e:
                raise ValueError(f'rank of {hyperedge} does not fit to rank {rule_to_inline.rank()} of {label}.')
        rule_to_inline = self[label]
        count_real_replacements = 0
        for rule_name in self:
            rule = self[rule_name]
            index = 0
            while index < len(rule):
                edge = rule[index]
                if edge.get_label() == label:
                    # new edge
                    edges = get_edges_for_hyperedge(edge)

                    # edge replacement. If more than one edge must be added, they are added at the end of the list.
                    # note, that these cannot have an occurrence of the current inlined rule (straight-line).
                    # This method takes care of this improvement.
                    # It can be further improved searching only in rules with lower numbers.
                    if len(edges) > 0:
                        rule[index] = edges[0]
                        rule.extend(edges[1:])
                        index += 1
                    else:
                        del rule[index]

                    # loop iteration updates: occurrences replacement loop
                    count_real_replacements += 1
                else:
                    index += 1

        del self[label]
        return count_real_replacements

    @average_timing
    def clone(self):
        """Clones this grammar objekt."""
        g = Grammar(self[self.get_start_rule_name()].clone(), self._terminal_func, self.terminal_rank, self.terminal_size)
        for rule_name in self:
            g[rule_name] = self[rule_name].clone()
        return g