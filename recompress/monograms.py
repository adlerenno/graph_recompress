from typing import Iterable

from classes.grammar.grammar import Grammar
from classes.grammar.graph import Graph
from classes.grams.monogram import Monogram
from classes.helper.count_dict import CountDict
from evaluate.timetest import log
from evaluate.timetest.average import average_timing


@average_timing
def replace_monograms(grammar):
    """Step 2: Monogram replacement. Custom Step for this Graph RePair."""

    # creates a dict mapping a monogram to its frequency of occurrence.
    rules = [grammar[rule_name] for rule_name in grammar if not grammar.is_terminal(rule_name)]
    monogram_count: CountDict = count_monograms(rules)

    # Main loop to replace monograms
    for monogram_to_replace in get_monogram_to_replace(monogram_count, grammar):
        monogram_to_replace.set_rule_name(grammar.get_unused_nonterminal())
        count_real_replacements = 0

        # loop to replace all occurrences
        for rule, old_edge, index in find_occurrence_of_monogram(monogram_to_replace, rules):
            if old_edge.get_label() == monogram_to_replace.get_label():
                new_edge = monogram_to_replace.apply_to_edge(old_edge)
                # edge replacement
                rule[index] = new_edge

                # update of frequencies
                update_monogram_dict(old_edge, new_edge, monogram_count, monogram_to_replace)

                # loop iteration updates: occurrences replacement loop
                count_real_replacements += 1

        log(f"Replaced {monogram_to_replace} for {count_real_replacements} times")

        # loop iteration updates: digram replacement loop
        if count_real_replacements > 0:
            new_rule: Graph = monogram_to_replace.create_rule(grammar)
            grammar.add_rule(monogram_to_replace.get_rule_name(), new_rule)

        # log(grammar)
        log(f'The total current size is {grammar.size_of_hole_grammar()}')


@average_timing
def count_monograms(rules):  # allow multiple_rules
    """This method creates a dict listing the rules with redundant Node IDs, e.g. ('B', 1, 2, 2).
    Returns a dict mapping a Monogram to a list of indices i, so that start_rule[i] is an occurrence of that monogram.
    """
    monogram_dict = CountDict()
    for rule in rules:
        for edge_id in range(len(rule)):
            e = rule[edge_id]
            nodes_connection_type_dict = {}

            # builds a dict mapping nodes to their connection_types of edge e
            for connection_type in range(e.rank()):
                node = e[connection_type]
                if node not in nodes_connection_type_dict:
                    nodes_connection_type_dict[node] = [connection_type]
                else:
                    nodes_connection_type_dict[node].append(connection_type)

            # loops through the nodes and all multiple named nodes.
            for node in nodes_connection_type_dict.keys():
                connection_type_list = nodes_connection_type_dict[node]
                if len(connection_type_list) > 1:
                    for i in range(len(connection_type_list)):
                        for j in range(i+1, len(connection_type_list)):
                            monogram = Monogram(e.get_label(), connection_type_list[i], connection_type_list[j])
                            monogram_dict[monogram] += 1
    return monogram_dict


def get_monogram_to_replace(monogram_count: CountDict, grammar: Grammar) -> Iterable[Monogram]:
    """Generator returning the most_frequent_monogram. All monograms are checked, if they should be replaced."""
    # get the most frequent rule
    monogram_to_replace: Monogram = monogram_count.get_max()

    # Main loop to replace monograms
    while should_continue_replacing_monogram(monogram_count, monogram_to_replace, grammar):
        yield monogram_to_replace
        if monogram_to_replace in monogram_count:
            del monogram_count[monogram_to_replace]
        monogram_to_replace = monogram_count.get_max()


@average_timing
def should_continue_replacing_monogram(monogram_dict, monogram_to_replace, grammar):
    """Here is the place, which decides if a replacement would reduce size.
    It should be used as a decision rule, not as a prediction.
    Returns a bool """
    if monogram_to_replace is None:
        return False
    n = monogram_dict[monogram_to_replace]
    g = grammar.rank_of_rule(monogram_to_replace.get_label()) + 1
    m = g - 1
    log(f'{monogram_to_replace} is counted {n} times. Old Rule size is {g}, new Rule size is {m}')
    return n * m + g < n * g


@average_timing
def find_occurrence_of_monogram(monogram_to_replace, rules):
    """Searches the next occurrence of a monogram within the start_rule
    Returns 1 indices pointing to the edge in the start_rule.

    We replace an edge with another one, so we can do this as a co-routine"""
    for rule in rules:
        for i, edge in enumerate(rule):
            if edge.get_label() == monogram_to_replace.get_label() \
                    and edge[monogram_to_replace[1]] == edge[monogram_to_replace[2]]:
                yield rule, edge, i


@average_timing
def update_monogram_dict(old_edge, new_edge, monogram_dict, replaced_monogram):
    """Updates the monogram_dict."""

    monogram_list = list(monogram_dict.keys())
    for monogram in monogram_list:

        # checks, if the Monogram is affected by the current replacement by testing,
        # in other words if the current edge is an occurrence of that monogram.
        if monogram.get_label() == old_edge.get_label() \
                and old_edge[monogram[1]] == old_edge[monogram[2]]:
            monogram_dict[monogram] -= 1
            # Check, if an occurrence must be a transform into one of a new monogram
            if monogram[1] != replaced_monogram[2] and monogram[2] != replaced_monogram[2]:
                first_type = monogram[1] - (0 if monogram[1] <= replaced_monogram[2] else 1)
                second_type = monogram[2] - (0 if monogram[2] <= replaced_monogram[2] else 1)
                if first_type < second_type:
                    new_monogram = Monogram(new_edge.get_label(), first_type, second_type)
                    monogram_dict[new_monogram] += 1
