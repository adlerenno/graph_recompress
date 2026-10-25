from classes.grammar.edge import Edge
from classes.grammar.grammar import Grammar
from evaluate.timetest import log
from evaluate.timetest.average import average_timing_name
from evaluate.timetest.normal import timing
from recompress.digrams import replace_digrams
from recompress.meta import MetaGrammar
from recompress.monograms import replace_monograms
from recompress.nograms import replace_nograms_or_prune
from recompress.pruning import prune

@timing
def recompress(grammar: Grammar) -> Grammar:
    """Use the GraphRePair recompression algorithmus.
    :param grammar: a grammar to recompress.
    :returns the newly compressed grammar.
    """
    # Stores information about the replacement process
    meta_grammar = MetaGrammar()
    start_rule_name = grammar.get_start_rule_name()
    log('The total size is {} of the not-recompressed grammar'.format(grammar.size_of_hole_grammar()))

    # Step 1: Digram replacing
    replace_digrams(grammar, start_rule_name, meta_grammar)

    # Step 2: Nogram Replacement or Pruning
    replace_nograms_or_prune(grammar, start_rule_name)

    # Step 3: Monogram Replacing
    replace_monograms(grammar)

    # make every rule visible for pruning
    grammar.clear_treat_as_terminal()

    # Step 4: Pruning
    prune(grammar, start_rule_name)

    # return the compressed grammar
    # log_average_times() Call this in the roundtrip instead!
    return grammar


@timing
def decompress(grammar: Grammar) -> Grammar:
    """This method decompresses a graph-grammar, so that there is no non-terminal anymore."""

    def get_edges_for_hyperedge(rule, hyperedge):
        """Creates edges for the hyperedge corresponding to the given Rule.

        :param rule:
        :param hyperedge: non-terminal of the rule given while this object is constructed.
        :returns the edges described by the given non-terminal.
        """
        return [Edge(e.get_label(), *[hyperedge[node] for node in e]) for e in rule.get_edges()]

    start_rule = grammar[grammar.get_start_rule_name()]
    i = 0
    while i < len(start_rule):
        if grammar.is_terminal(start_rule[i].get_label()):
            i += 1
        else:
            # Found a non-terminal. Inline it.
            new_edges = get_edges_for_hyperedge(grammar[start_rule[i].get_label()], start_rule[i])
            del start_rule[i]
            start_rule.extend(new_edges)
    grammar.delete_all_rules_except_start_rule()
    return grammar

