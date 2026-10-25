from typing import List, Dict, Set, Iterable

from classes.grammar.edge import Edge
from classes.grammar.grammar import Grammar
from classes.grammar.graph import Graph
from classes.grammar.path import Path
from classes.grams.digram import Digram, DigramOccurrence
from classes.helper.count_dict import CountDict
from classes.helper.dag import DAGNode
from evaluate.timetest import log
from evaluate.timetest.average import average_timing
from recompress.nograms import replace_nograms_or_prune
from recompress.meta import MetaGrammar, MetaGraph, PathDict


@average_timing
def replace_digrams(grammar: Grammar, start_rule_name, meta: MetaGrammar):
    """TODO: write tests"""
    for most_frequent_digram in get_digrams_to_replace(grammar, meta, start_rule_name):
        # find occurrences
        find_all_occurrences_of_digram(grammar, start_rule_name, most_frequent_digram, meta)

        log(f'Found {len(meta.get_occurrences())} non-overlapping occurrences')

        # check if there is something to replace
        if len(meta.get_occurrences()) > 0:  # TODO: find better condition here! Regard: there are occurrences replacing multiple occurrences at one time...

            # reduce the size of the dag from a tree to a real dag by finding fitting equal nodes.
            meta_start_rule = meta.get_meta(start_rule_name)
            meta_start_rule.get_dag().minimize()
            log(f'DAG has {len(meta_start_rule.get_dag().get_nodes())} nodes')

            #  Introduce new rule name for mfd. Treat it as terminal as long as digrams and monograms are replaced.
            new_rule_name = grammar.get_unused_nonterminal()
            most_frequent_digram.set_rule_name(new_rule_name)
            grammar[new_rule_name] = most_frequent_digram.create_rule(grammar)
            grammar.add_treat_as_terminal(new_rule_name)

            # Replace the digrams:
            # 1. isolate edges and create their corresponding nonterminals
            replace_digram_occurrences(grammar, most_frequent_digram, meta)

            # 2. introduce new help rules (smart isolation)
            create_help_rules_for_removing_edges(grammar, meta_start_rule)

            # 3. delete edges from grammar by changing nonterminal use and mark as delete.
            remove_used_edges_from_grammar(grammar, meta_start_rule)

            # Step 2: Nogram Replacement or Pruning
            replace_nograms_or_prune(grammar, start_rule_name)

        # log(grammar)
        log(f'The total current size is {grammar.size_of_hole_grammar()}')


@average_timing
def count_digrams(grammar: Grammar, meta: MetaGrammar, start_rule_name) -> CountDict:
    """
    :param meta: MetaObject storing information about the grammar
    :param grammar: grammar to count digrams in.
    :return: a CountDict, with Digrams as keys and ints representing the calculated frequencies of them.
    """
    inline_nonterminal_adjacency(start_rule_name, grammar, meta)
    return calculate_digrams_from_node_edge_adjacency_dict(meta.get_meta(start_rule_name).get_node_edge_adjacency_dict())


@average_timing
def inline_nonterminal_adjacency(rule_name, grammar: Grammar, meta: MetaGrammar):
    """inlines recursively the adjacency of nonterminals."""
    meta_graph: MetaGraph = meta.get_meta(rule_name)
    node_edge_adjacency_dict = meta_graph.get_node_edge_adjacency_dict()
    if node_edge_adjacency_dict is not None:
        # This case is the recursion anchor as well as terminal symbols
        return
    else:
        node_edge_adjacency_dict = grammar[rule_name].get_node_edge_adjacency_dict()
        meta_graph.set_node_edge_adjacency_dict(node_edge_adjacency_dict)
        # Inlining must be done for each node
        for node in node_edge_adjacency_dict:
            adjacency_frequencies = node_edge_adjacency_dict[node]

            # Replacement must be done for each adjacency_type
            for adjacency_type in list(adjacency_frequencies.keys()):
                label, connection_type = adjacency_type

                # it is not necessary to do anything if it's a terminal already
                if not grammar.is_terminal(label):

                    # Check if the rule is inserted already, so it only contains terminal-adjacency_types
                    # recursion call is here
                    inline_nonterminal_adjacency(label, grammar, meta)
                    node_edge_adjacency_dict_of_nonterminal = meta.get_meta(label).get_node_edge_adjacency_dict()

                    # Insert the adjacency_type_frequencies from the rule label
                    adjacency_frequencies_to_add = node_edge_adjacency_dict_of_nonterminal[connection_type]
                    factor = adjacency_frequencies[adjacency_type]
                    for adjacency_type_to_add in adjacency_frequencies_to_add:
                        adjacency_frequencies[adjacency_type_to_add] += \
                            factor * adjacency_frequencies_to_add[adjacency_type_to_add]
                    del adjacency_frequencies[adjacency_type]


@average_timing
def calculate_digrams_from_node_edge_adjacency_dict(node_edge_adjacency_dict: dict) -> CountDict:
    """Returns a dictionary mapping digrams to their occurrence-frequency (ideally) """
    digram_count = CountDict()
    for node in node_edge_adjacency_dict.keys():
        adjacency_type_dict = node_edge_adjacency_dict[node]
        keys = list(adjacency_type_dict.keys())
        adjacency_type_count = len(keys)
        # consider each pair of AdjacencyTypes at the given node as a digram.
        # Note, that digrams should have no oder of AdjacencyTypes.
        for i in range(adjacency_type_count):
            for j in range(i+1, adjacency_type_count):
                _update_digram_count(digram_count, Digram(keys[i], keys[j]), min(adjacency_type_dict[keys[i]], adjacency_type_dict[keys[j]]))
            # consider each self-pair as well. Note: it has another way of counting.
            _update_digram_count(digram_count, Digram(keys[i], keys[i]), adjacency_type_dict[keys[i]] // 2)
    return digram_count


@average_timing
def _update_digram_count(digram_count, digram, delta):
    """Updates the entry digram of digram_count by delta. Order of AdjacencyTypes does not matter for the update."""
    inverted_digram = digram.invert()
    if digram in digram_count:
        digram_count[digram] += delta
    elif inverted_digram in digram_count:
        digram_count[inverted_digram] += delta
    elif delta > 0:
        digram_count[digram] = delta


@average_timing
def _set_digram_count(digram_count, digram, new_value):
    """Updates the entry digram of digram_count by delta. Order of AdjacencyTypes does not matter for the update."""
    inverted_digram = digram.invert()
    if digram in digram_count:
        digram_count[digram] = new_value
    elif inverted_digram in digram_count:
        digram_count[inverted_digram] = new_value
    elif new_value > 0:
        digram_count[digram] = new_value


@average_timing
def get_digrams_to_replace(grammar: Grammar, meta: MetaGrammar, start_rule_name: int) -> Iterable[Digram]:
    """ Generator generating the most_frequent_digram. Recounts every time and calls meta.clear()"""
    already_replaced_digrams = []

    # find most frequent digram
    digram_count: CountDict = count_digrams(grammar, meta, start_rule_name)
    most_frequent_digram: Digram = digram_count.get_max()
    while should_continue_replacing_digram(most_frequent_digram, digram_count, grammar):
        yield most_frequent_digram
        # loop updates
        already_replaced_digrams.append(most_frequent_digram)
        digram_count = count_digrams(grammar, meta, start_rule_name)

        # ensure to not select a digram twice
        for mfd in already_replaced_digrams:
            _set_digram_count(digram_count, mfd, 0)

        # select new mfd
        meta.clear()
        most_frequent_digram: Digram = digram_count.get_max()


@average_timing
def should_continue_replacing_digram(digram, digram_count, grammar):
    """Here is the place, which decides if a replacement would reduce size.
    It should be used as a decision rule, not as a prediction.
    Returns true, if it should be replaced. """
    if digram is None:
        return False
    n = digram_count[digram]
    g = grammar.rank_of_rule(digram[0].get_label()) + 1 + grammar.rank_of_rule(digram[1].get_label()) + 1
    m = g - 2
    log(f'{digram} is counted {n} times. Old Rule size is {g}, new Rule size is {m}')
    return n * m + g < n * g


@average_timing
def find_all_occurrences_of_digram(grammar: Grammar, rule_name, digram: Digram, meta: MetaGrammar):
    """:returns a pair of paths and a dag.
    in the dag, there are all paths that are already used to generate occurrences of digrams
    occurrences of digrams are added to meta.
    the paths contain a PathDict object, that maps adjacency_types to dicts, who are mapping a node to a list of paths
    works recursively and use the visit field to mark rules with are evaluated already."""
    meta_graph = meta.get_meta(rule_name)
    if meta_graph.is_visited():
        return meta_graph.get_paths(), meta_graph.get_dag()
    else:
        meta_graph: MetaGraph = meta.get_meta(rule_name)
        meta_graph.visit()
        for position_of_edge, edge in enumerate(grammar[rule_name]):
            if edge.get_label() == digram[0].get_label():
                meta_graph.add_path(digram[0], edge[digram[0].get_connection_type()], Path(position_of_edge, edge.get_label()))
            if edge.get_label() == digram[1].get_label() and digram[0] != digram[1]:
                meta_graph.add_path(digram[1], edge[digram[1].get_connection_type()], Path(position_of_edge, edge.get_label()))
            if not grammar.is_terminal(edge.get_label()):
                paths, dag = find_all_occurrences_of_digram(grammar, edge.get_label(), digram, meta)
                meta_graph.get_paths().extend(paths.add_before(edge, position_of_edge))
                if not dag.is_empty():
                    meta_graph.get_dag().add_sub_dag(Path(position_of_edge, edge.get_label()), dag.deep_copy())
        build_occurrences(digram, meta_graph, meta, rule_name)
        return meta_graph.get_paths(), meta_graph.get_dag()


@average_timing
def build_occurrences(digram: Digram, meta_graph: MetaGraph, meta_grammar: MetaGrammar, rule_name):
    """Generates DigramOccurrences by a given paths dict."""
    paths: PathDict = meta_graph.get_paths()
    if digram[0] != digram[1]:  # digrams of form ((a, l), (b, m)) or ((a, l), (a, m))
        if len(paths.get_adjacency_types()) < 2:
            return
        for vertex in paths[digram[0]]:
            try:
                paths_of_type_0 = paths[digram[0]][vertex]
                paths_of_type_1 = paths[digram[1]][vertex]
            except KeyError:
                # Indicates, that one of the lists does not exist, so there are no occurrences
                continue
            found_0, found_1 = len(paths_of_type_0) is not 0, len(paths_of_type_1) is not 0
            while found_0 and found_1:  # both contain at least another path
                # paths_of_type_0.sort()  # TODO: sort paths here, may reduce the amount of isolation
                # paths_of_type_1.sort()
                pos_0, pos_1 = 0, 0
                while found_0 and meta_graph.get_dag().has_path(paths_of_type_0[pos_0]):
                    pos_0 += 1
                    if pos_0 >= len(paths_of_type_0):
                        found_0 = False
                if found_0:
                    while found_1 and (meta_graph.get_dag().has_path(paths_of_type_1[pos_1])
                                       or paths_of_type_0[pos_0] == paths_of_type_1[pos_1]):
                        pos_1 += 1
                        if pos_1 >= len(paths_of_type_1):
                            found_1 = False

                # keep pair
                if found_0 and found_1:
                    meta_grammar.add_occurrence(DigramOccurrence(digram, paths_of_type_0[pos_0], paths_of_type_1[pos_1], rule_name))
                    meta_graph.get_dag().add_path(paths_of_type_0[pos_0])
                    meta_graph.get_dag().add_path(paths_of_type_1[pos_1])

                    # remove paths from lists
                    for _ in range(pos_0 + 1):
                        del paths_of_type_0[0]

                    for _ in range(pos_1 + 1):
                        del paths_of_type_1[0]

                found_0 = found_0 and len(paths_of_type_0) is not 0
                found_1 = found_1 and len(paths_of_type_1) is not 0
    else:  # digrams of from ((a, l), (a, l))
        if len(paths.get_adjacency_types()) < 1:
            return
        for vertex in paths[digram[0]]:
            try:
                paths_of_type_0 = paths[digram[0]][vertex]
            except KeyError:
                # Indicates, that one of the lists does not exist, so there are no occurrences
                continue
            found_0, found_1 = len(paths_of_type_0) is not 0, len(paths_of_type_0) is not 0
            while found_0 and found_1:  # both contain at least another path
                # paths_of_type_0.sort()  # TODO: sort paths here, may reduce the amount of isolation
                pos_0 = 0
                while meta_graph.get_dag().has_path(paths_of_type_0[pos_0]) and found_0:
                    pos_0 += 1
                    if pos_0 >= len(paths_of_type_0):
                        found_0 = False
                pos_1 = pos_0 + 1
                if found_0:
                    found_1 = found_1 and pos_1 < len(paths_of_type_0)
                    while found_1 and (meta_graph.get_dag().has_path(paths_of_type_0[pos_1])
                                       or paths_of_type_0[pos_0] == paths_of_type_0[pos_1]):
                        pos_1 += 1
                        if pos_1 >= len(paths_of_type_0):
                            found_1 = False

                # keep pair
                if found_0 and found_1:
                    meta_grammar.add_occurrence(DigramOccurrence(digram, paths_of_type_0[pos_0], paths_of_type_0[pos_1], rule_name))
                    meta_graph.get_dag().add_path(paths_of_type_0[pos_0])
                    meta_graph.get_dag().add_path(paths_of_type_0[pos_1])

                    # remove paths from lists
                    for _ in range(pos_1 + 1):
                        del paths_of_type_0[0]

                found_0 = found_0 and len(paths_of_type_0) is not 0
                found_1 = found_1 and len(paths_of_type_0) is not 0


@average_timing
def replace_digram_occurrences(grammar: Grammar, most_frequent_digram: Digram, meta: MetaGrammar):
    """isolate edges and create their corresponding nonterminals for occurrences listed in meta.
    calls rule_changed of meta_rules, if nonterminals are added. """
    for occurrence in meta.get_occurrences():
        edge_0 = grammar.isolate_edge(occurrence.get_occurring_rule_name(), occurrence.get_path_to_adjacency_type_0())
        edge_1 = grammar.isolate_edge(occurrence.get_occurring_rule_name(), occurrence.get_path_to_adjacency_type_1())
        hyperedge = most_frequent_digram.apply_to_edges(edge_0, edge_1)
        grammar[occurrence.get_occurring_rule_name()] += hyperedge

        # ensure that all rules where digrams are replaced are that they are changed
        meta.get_meta(occurrence.get_occurring_rule_name()).rule_changed()


@average_timing
def create_help_rules_for_removing_edges(grammar: Grammar, meta_start_rule: MetaGraph):
    """TODO: method is not very efficient yet, because it does not update directly. """
    nodes = meta_start_rule.get_dag().get_nodes_except_head()
    affected_rule_names = {node.get_name() for node in nodes}
    name_to_nodes: Dict[int, Set[DAGNode]] = {name: set() for name in affected_rule_names}
    for node in nodes:
        name_to_nodes[node.get_name()].add(node)
    for name in affected_rule_names:
        all_affected_positions = set()
        for node in name_to_nodes[name]:
            all_affected_positions.update(node.get_path_ends())
            all_affected_positions.update(node.get_next_positions())
        all_affected_positions = list(all_affected_positions)
        all_affected_positions.sort()

        old_rule = grammar[name]
        if len(old_rule) == len(all_affected_positions):  # all edges are affected, no base rule created
            base_rule_name = None
            nonterminal_to_base = None
            need_base_rule_delete = False
        else:
            base_rule_name = add_rule_to_grammar(grammar, old_rule)
            nonterminal_to_base = Edge(base_rule_name, nodes=range(old_rule.rank()))
            need_base_rule_delete = True
            log(f'Add {base_rule_name} as base rule')

        # for each node in the dag exactly one rule is created
        for node in name_to_nodes[name]:
            if len(node.get_path_ends()) == len(all_affected_positions):  # all will be deleted, except base maybe
                if nonterminal_to_base is not None:
                    node.set_new_name(base_rule_name)  # directly use base rule instead.
                    need_base_rule_delete = False  # no delete needed anymore
                else:
                    node.set_new_name(None)  # no rule will be created.
            else:
                new_rule = create_smart_inlined_help_rule(old_rule, all_affected_positions, nonterminal_to_base)
                node.set_new_name(add_rule_to_grammar(grammar, new_rule))
                log(f'Add {node.get_new_name()} as new rule for node {node}: {new_rule}')
                node.update_path_symbols(all_affected_positions)
        if nonterminal_to_base is not None:  # only update rule if necessary
            grammar[name] = create_smart_inlined_help_rule(old_rule, all_affected_positions, nonterminal_to_base)
            log(f'Update {name} to use base rule {nonterminal_to_base.get_label()}: {grammar[name]}')

            # if base rule is used from a dag_node directly, the deletion will be in the next step.
            if need_base_rule_delete:
                # make old rule to base rule.
                for index in all_affected_positions[::-1]:
                    del old_rule[index]
                log(f'base rule: {old_rule}')


@average_timing
def create_smart_inlined_help_rule(old_rule: Graph, positions: List[int], edge: Edge):
    """ Creates a Graph object copying the edges from :param old_rule: from the positions definied in :param positions:
    if edge is not None, the edge, which should be the base rule, is also copied to the new graph.
    TODO:do not copy edges we do not need (node.path_ends)"""
    new_edges = list(map(lambda x: x[1].clone(), filter(lambda x: x[0] in positions, enumerate(old_rule.get_edges()))))
    if edge is not None:
        new_edges.append(edge.clone())
    return Graph(new_edges, old_rule.rank())


def add_rule_to_grammar(grammar: Grammar, rule: Graph):
    """Help method to add a rule to the grammar object and returns the new name."""
    help_rule_name = grammar.get_unused_nonterminal()
    grammar[help_rule_name] = rule
    return help_rule_name


@average_timing
def remove_used_edges_from_grammar(grammar: Grammar, meta_start_rule: MetaGraph):
    """delete edges from grammar by changing nonterminal use and mark as delete of path_ends (using helper method
     update_rule_by_dag_node).
    Iterates over the dag_nodes and the whole grammar to delete."""
    for dag_node in meta_start_rule.get_dag().get_nodes_except_head():
        update_rule_by_dag_node(grammar, dag_node.get_new_name(), dag_node)

    # do head separat. use dag_node.get_name instead of dag_node.get_new_name, because no new start rule is created.
    dag_node = meta_start_rule.get_dag().get_head()
    update_rule_by_dag_node(grammar, dag_node.get_name(), dag_node)

    # remove path_end edges
    grammar.delete_all_mark_as_delete_edges()


@average_timing
def update_rule_by_dag_node(grammar: Grammar, rule_name: int, dag_node: DAGNode):
    """helper_method for remove_used_edges_from_grammar."""
    if rule_name is None:
        return
    for path_end in dag_node.get_path_ends():
        # mark as delete the edge
        grammar[rule_name].get_edges()[path_end].mark_as_delete()
    for next_position_of_nonterminal_to_update in dag_node.get_next_positions():
        # change label of rule from next node name to next node new name
        edge_to_update: Edge = grammar[rule_name].get_edges()[next_position_of_nonterminal_to_update]
        edge_to_update.change_label(dag_node.get_next(next_position_of_nonterminal_to_update).get_new_name())
