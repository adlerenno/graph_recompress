from typing import Generator

from classes.grammar.grammar import Grammar
from classes.grammar.graph import Graph
from classes.grams.nogram import Nogram
from classes.helper.bitvector import Bitvector
from classes.helper.count_dict import CountDict
from evaluate.timetest import log

from evaluate.timetest.average import average_timing
import recompress.pruning as pruning


@average_timing
def replace_nograms_or_prune(grammar, start_rule_name):
    """Step 2: Nogram replacement. Custom Step for this Graph RePair."""

    rules_count: CountDict = pruning.count_rules(grammar)
    pruning.remove_not_occurring_rules(grammar, rules_count, start_rule_name)

    # Main loop to replace nograms or inline rules.
    for nogram_to_replace in get_nograms_to_replace(grammar, start_rule_name):
        # decide if prune or nogram is the correct handling. TODO: not correct condition yet.
        if pruning.should_inline_rule(nogram_to_replace.get_label(), rules_count, grammar):
            log(f'Inline rule {nogram_to_replace.get_label()}')
            pruning.inline_rule(nogram_to_replace.get_label(), rules_count, grammar)
        else:
            log(f'Replace nogram {nogram_to_replace}')
            new_rule = nogram_to_replace.create_rule(grammar)
            grammar[nogram_to_replace.get_label()] = new_rule

            count_real_replacements = 0
            for rule, edge, index in find_occurrence_of_nogram(nogram_to_replace, grammar):
                rule[index] = nogram_to_replace.apply_to_edge(edge)
                count_real_replacements += 1

            # each symbol only needs to be visited once
            if nogram_to_replace.get_label() in rules_count:
                del rules_count[nogram_to_replace.get_label()]

            log(f"Replaced {nogram_to_replace} for {count_real_replacements} times")

        # log(grammar)
        log(f'The total current size is {grammar.size_of_hole_grammar()}')

    # prune with the rest of the count
    pruning.prune(grammar, start_rule_name, rules_count)


@average_timing
def get_nograms_to_replace(grammar: Grammar, start_rule_name: int) -> Generator[Nogram, None, None]:
    """Generator generating nograms of the grammar. Nograms are only returned if there is at least one
    unused parameter. TODO: no nograms from rules containing a nonterminal of a later replaced nogram are returned."""
    for rule_name in list(grammar.__iter__()):
        if rule_name is not start_rule_name:
            rule: Graph = grammar[rule_name]
            nogram: Nogram = Nogram(rule_name, Bitvector(rule.rank()))
            nogram.by_rule(grammar)
            if nogram.should_replace():
                yield nogram


@average_timing
def find_occurrence_of_nogram(nogram_to_replace: Nogram, grammar: Grammar):
    """Generator returning a rule and an index. At that destination is an occurrence of a nogram."""
    for rule_name in grammar:
        rule: Graph = grammar[rule_name]
        for i, edge in enumerate(rule):
            if edge.get_label() == nogram_to_replace.get_label():
                yield rule, edge, i
