import random

from classes.grammar.edge import Edge
from classes.grammar.grammar import Grammar
from classes.grammar.graph import Graph


def random_base_2_grammar(node_count, edge_count, edge_label):
    """Generates a Graph object with node_count nodes and edge_count normal edges.
    Uses a random edge_label.
    :param node_count: maximal amount of nodes in the generated graph.
    :param edge_count: exact count of edges in the generated graph. All edges will have rank 2.
    :param edge_label: all possible labels of the edges. Is an label more than ones in this, it appears more often.
    :returns the grammar. """
    edge_list = [Edge(random.choice(edge_label), random.randrange(node_count), random.randrange(node_count))
                 for _ in range(edge_count)]
    graph = Graph(edge_list)
    return Grammar(graph, lambda x: x in edge_label, lambda x: 2, lambda x: 3)


def random_base_grammar(node_count, edge_count, edge_label, label_rank_dict):
    """Generates a Graph object with node_count nodes and edge_count normal edges.
    Uses a random edge_label.
    :param node_count: maximal amount of nodes in the generated graph.
    :param edge_count: exact count of edges in the generated graph.
    :param edge_label: all possible labels of the edges. Is a label more than ones in this, it appears more often.
    :param label_rank_dict: each edge_label should have a rank defined by this parameter.
    :returns the grammar. """
    graph = random_hypergraph(node_count, edge_count, edge_label, label_rank_dict)
    return Grammar(graph, lambda x: x in edge_label, lambda x: label_rank_dict[x], lambda x: label_rank_dict[x]+1)


def random_hypergraph(node_count, edge_count, edge_label, label_rank_dict):
    node_count = max(node_count, 3)
    edge_list = []
    for _ in range(edge_count):
        label = random.choice(edge_label)
        rank = label_rank_dict[label]
        edge_list.append(Edge(label, *(random.randrange(node_count) for _1 in range(rank))))
    graph = Graph(edge_list, rank=node_count)
    return graph


def random_grammar(node_count, edge_count, rule_count, edge_label, label_rank_dict):
    """ :param node_count: defines the nodes of the start_rule.
    :param edge_count: defines the number of edges through the complete grammar.
    :param rule_count: defines the number of rules generated.
    :param edge_label: defines the terminal symbols
    :param label_rank_dict: defines the ranks of terminal symbols."""
    rules = {e: None for e in edge_label}
    ed = edge_count // rule_count
    for _ in range(rule_count):
        graph = random_hypergraph(ed//2, ed, list(rules.keys()), label_rank_dict)
        name = get_number_not_in(rules.keys())
        rules[name] = graph
        label_rank_dict[name] = graph.rank()

    g = Grammar(random_hypergraph(node_count, ed, list(rules.keys()), label_rank_dict),
                lambda x: x in edge_label, lambda x: label_rank_dict[x], lambda x: label_rank_dict[x]+1)
    for rule_name in rules:
        if rule_name not in edge_label and rule_name is not 0:
            g[rule_name] = rules[rule_name]
    return g


def random_3_grammar(node_count, edge_count, rule_count, edge_label, label_rank_dict):
    """ :param node_count: defines the nodes of the start_rule.
    :param edge_count: defines the number of edges through the complete grammar.
    :param rule_count: defines the number of rules generated.
    :param edge_label: defines the terminal symbols
    :param label_rank_dict: defines the ranks of terminal symbols."""
    rules = {e: None for e in edge_label}
    ed = edge_count // rule_count
    for _ in range(rule_count):
        graph = random_hypergraph(5, 3, list(rules.keys()), label_rank_dict)
        name = get_number_not_in(rules.keys())
        rules[name] = graph
        label_rank_dict[name] = graph.rank()

    g = Grammar(random_hypergraph(node_count, ed, list(rules.keys()), label_rank_dict),
                lambda x: x in edge_label, lambda x: label_rank_dict[x], lambda x: label_rank_dict[x]+1)
    for rule_name in rules:
        if rule_name not in edge_label and rule_name is not 0:
            g[rule_name] = rules[rule_name]
    return g


def get_number_not_in(iter):
    i = 1
    while i in iter:
        i += 1
    return i