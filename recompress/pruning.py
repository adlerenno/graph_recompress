from typing import Iterable

from classes.grammar.grammar import Grammar
from classes.grammar.graph import Graph
from classes.helper.count_dict import CountDict
from evaluate.timetest import log
from evaluate.timetest.average import average_timing


@average_timing
def prune(grammar: Grammar, start_rule_name: int, rule_dict: CountDict = None):
    """ Step 3: Prune the grammar. All rules are tested, if they are efficient to the size of the grammar.
    If not, inline them."""

    # optional parameter used by nogram replacement to do the rest of the pruning.
    if rule_dict is None:
        # creates a dict mapping a Rule label to its frequencies.
        rule_dict = count_rules(grammar)

        # once: delete all rules without a nonterminal who reference it
        remove_not_occurring_rules(grammar, rule_dict, start_rule_name)

    # Main loop: Pruning
    for rule_name_to_inline in get_rules_to_inline(rule_dict, grammar):
        inline_rule(rule_name_to_inline, rule_dict, grammar)

        # log(grammar)
        log(f'The total current size is {grammar.size_of_hole_grammar()}')


@average_timing
def count_rules(grammar: Grammar) -> CountDict:
    """Returns a dict mapping a rule_name to its usage frequency.
    Start Rule and terminals are not included within the dict"""
    rule_dict = CountDict()
    # count every edge in all Rules (start rule never named -> not included)
    for rule in grammar:
        edges = grammar[rule]
        for edge in edges:
            rule_dict[edge.get_label()] += 1
    # delete all terminals, so they will not be replaced.
    for rule_name in list(rule_dict.keys()):
        if grammar.is_terminal(rule_name):
            del rule_dict[rule_name]
    return rule_dict


@average_timing
def remove_not_occurring_rules(grammar: Grammar, rules_count: CountDict, start_rule_name: int):
    """Removes all rules, that do not occur in rules_count and are neither the start rule nor a terminal from the
    grammar. TODO: delete rules, that had one occurrence but do not have an occurrence after removing another rule."""
    for rule_name in list(grammar.__iter__()):
        if rule_name not in rules_count and rule_name != start_rule_name and not grammar.is_terminal(rule_name):
            # delete rule and update count of others.
            update_rule_dict(rules_count, grammar[rule_name], 0, grammar)
            del grammar[rule_name]

            log(f'removed {rule_name} from grammar, because it has no occurrence')


@average_timing
def get_rules_to_inline(rule_dict: CountDict, grammar: Grammar) -> Iterable[int]:
    """Generator, that returns all rule names that should be inlined. Order by occurrence count of rule_dict.
    Least occurrence count first."""
    while len(rule_dict.keys()) > 0:
        rule_name_to_inline = rule_dict.get_min()
        if should_inline_rule(rule_name_to_inline, rule_dict, grammar):
            yield rule_name_to_inline
        else:
            del rule_dict[rule_name_to_inline]


@average_timing
def should_inline_rule(rule_name_to_inline: int, rule_dict: CountDict, grammar: Grammar) -> bool:
    """Returns true, if the current rule makes the grammar bigger than it would be when the rule is inlined. """
    if rule_name_to_inline is None:
        return False
    frequency = rule_dict[rule_name_to_inline]
    used_size = grammar.rank_of_rule(rule_name_to_inline) + 1
    rule_size = grammar.size_of_rule(rule_name_to_inline)
    log(f'{rule_name_to_inline} is counted {frequency} times. Used size is {used_size}, Rule size is {rule_size}')
    return frequency * used_size + rule_size > frequency * rule_size


@average_timing
def inline_rule(rule_name_to_inline: int, rule_dict: CountDict, grammar: Grammar):
    rule_to_inline = grammar[rule_name_to_inline]

    # Replacement. Searches an occurrences of the rule.
    count_real_replacements = grammar.inline_rule(rule_name_to_inline)
    log(f"Replaced {rule_name_to_inline} for {count_real_replacements} times")

    # loop iteration updates: pruning loop
    update_rule_dict(rule_dict, rule_to_inline, count_real_replacements, grammar)
    if rule_name_to_inline in rule_dict:
        del rule_dict[rule_name_to_inline]


@average_timing
def update_rule_dict(rule_dict: CountDict, rule_to_inline: Graph, count_real_replacements: int, grammar: Grammar):
    """Updates the rule_dict so that the number of occurrence is still correct"""
    for edge in rule_to_inline:
        if not grammar.is_terminal(edge.get_label()):
            # rule is inlined count_real_replacements times, but the rule is deleted, so it occurs one time less.
            rule_dict[edge.get_label()] += count_real_replacements - 1

