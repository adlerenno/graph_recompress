from classes.grammar.edge import Edge
from classes.grammar.grammar import Grammar
from classes.grammar.graph import Graph


def bsp1():
    s = Graph([Edge(1, 0, 1, 2), Edge(1, 2, 3, 4), Edge(2, 1, 3, 0),
               Edge(3, 0, 1, 2), Edge(3, 2, 3, 4), Edge(4, 1, 3, 0)], rank=5)
    a = Graph([Edge(2, 0, 1, 2), Edge('a', 2, 1)], rank=3)
    b = Graph([Edge('a', 0, 1), Edge('a', 0, 2)], rank=3)
    c = Graph([Edge(4, 0, 1, 2), Edge('b', 2, 1)], rank=3)
    d = Graph([Edge('b', 0, 1), Edge('b', 0, 2)], rank=3)
    g = Grammar(s, lambda x: x in {'a', 'b'}, lambda x: 2, lambda x: 3)
    g.add_rule(1, a)
    g.add_rule(2, b)
    g.add_rule(3, c)
    g.add_rule(4, d)
    return g
