from graphrepair import *


def generate_tree(depth):
    """Generates a binary tree with normal edges."""
    edges = _generate_tree(depth, 1)
    G = Graph(edges)
    return G


def generate_tree_hyperedge(depth):
    """Generates a binary tree with rank 3 edges."""
    edges = _generate_tree_hyperedge(depth, 1)
    G = Graph()
    G._edges = edges
    return G


def _generate_tree(depth, root):
    """Recursively generates binary trees by using two simple edges."""
    if depth is 0:
        return []
    left = _generate_tree(depth-1, 2*root)
    right = _generate_tree(depth-1, 2*root+1)
    return [Edge('a', root-1, 2*root-1), Edge('b', root-1, 2*root), Edge('a', 2*root-1, root-1), Edge('b', 2*root, root-1)] + left + right


def _generate_tree_hyperedge(depth, root):
    """Recursively generates binary trees by using a single rank 3 edge."""
    if depth is 0:
        return []
    left = _generate_tree_hyperedge(depth-1, 2*root)
    right = _generate_tree_hyperedge(depth-1, 2*root+1)
    return [Edge('A', root-1, 2*root-1, 2*root)] + left + right


def generate_loops(node_count):
    """Generates a graph with node_count nodes each with a loops of rank 3.
    :param node_count: number of nodes (and of edges)"""
    G = Graph()
    G._edges = [Edge('a', i, i, i) for i in range(node_count)]
    return G


def generate_diloops(node_count):
    """Generates a graph with node_count nodes each with a simple loop.
    :param node_count: number of nodes (and of edges)"""
    G = Graph()
    G._edges = 2 * [Edge('a', i, i) for i in range(node_count)]
    return G
