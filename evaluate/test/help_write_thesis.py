from classes.grammar.edge import Edge
from classes.grammar.grammar import Grammar
from classes.grammar.graph import Graph
from evaluate.test import bsp1
from recompress import MetaGrammar, decompress, recompress
from recompress.digrams import count_digrams

S = Graph([Edge(1, 0, 1, 2), Edge('a', 1, 2), Edge(1, 3, 4, 5)], rank=6)
C = Graph([Edge(2, 0, 1), Edge('a', 0, 2)], 2)
D = Graph([Edge('b', 0, 1), Edge('b', 0, 1)])
G = Grammar(S, lambda x: x in ['a', 'b'], lambda x: 2, lambda x: 3)
G.add_rule(1, C)
G.add_rule(2, D)

print(count_digrams(G, MetaGrammar(), 0))


grammar = bsp1()

print(grammar)
meta_grammar = MetaGrammar()
# replace_digrams(self.grammar, 0, meta_grammar)
recompress(grammar)
print(grammar)
print(grammar.size_of_hole_grammar())
grammar.clear_treat_as_terminal()
decompress(grammar)
print(grammar)
print(grammar.size_of_hole_grammar())