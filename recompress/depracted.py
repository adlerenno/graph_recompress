from classes.grammar.grammar import Grammar
from evaluate.timetest.average import average_timing
from recompress.digrams import calculate_digrams_from_node_edge_adjacency_dict


@average_timing
def count_digrams(grammar: Grammar):
    """

    :param grammar: grammar to count digrams in.
    :return: a CountDict, with Digrams as keys and ints representing the calculated frequencies of them.
    """
    affected_rules = {rule_name for rule_name in grammar}
    rules_adjacency = {rule_name: grammar[rule_name].get_node_edge_adjacency_dict() for rule_name in grammar}

    def inline_nonterminal_adjacency(rule_name):
        if rule_name not in affected_rules:
            return
        else:
            node_edge_adjacency_dict = rules_adjacency[rule_name]

            # Inlining must be done for each node
            for node in node_edge_adjacency_dict:
                adjacency_frequencies = node_edge_adjacency_dict[node]

                # Replacement must be done for each adjacency_type
                for adjacency_type in list(adjacency_frequencies.keys()):
                    label, connection_type = adjacency_type

                    # it is not necessary to do anything if it's a terminal already
                    if not grammar.is_terminal(label):
                        node_edge_adjacency_dict_of_nonterminal = rules_adjacency[label]

                        # Check if the rule is added later and make sure it appears in  rules_adjacency
                        if node_edge_adjacency_dict_of_nonterminal is None:
                            node_edge_adjacency_dict_of_nonterminal = grammar[label].get_node_edge_adjacency_dict()
                            rules_adjacency[label] = node_edge_adjacency_dict_of_nonterminal

                        # Check if the rule is inserted already, so it only contains terminal-adjacency_types
                        if label in affected_rules:
                            inline_nonterminal_adjacency(label)

                        # Insert the adjacency_type_frequencies from the rule label
                        adjacency_frequencies_to_add = node_edge_adjacency_dict_of_nonterminal[connection_type]
                        factor = adjacency_frequencies[adjacency_type]
                        for adjacency_type_to_add in adjacency_frequencies_to_add:
                            adjacency_frequencies[adjacency_type_to_add] += \
                                factor * adjacency_frequencies_to_add[adjacency_type_to_add]
                        del adjacency_frequencies[adjacency_type]

            # ensures that the inline is only done once.
            affected_rules.remove(rule_name)

    while True:
        # inline the start rule
        inline_nonterminal_adjacency(0)

        # Use start rule only to calculate digrams
        affected_rules = yield calculate_digrams_from_node_edge_adjacency_dict(rules_adjacency[0])

        # start_rule has to be recalculated.
        affected_rules += {0}
        rules_adjacency[0] = grammar[grammar.get_start_rule_name()].get_node_edge_adjacency_dict()