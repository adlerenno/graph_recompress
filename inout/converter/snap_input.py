import snap
from classes import *


def read(file_name):
    """Should read some graphs from http://snap.stanford.edu/index.html . Not jet working. Needs packages via pip (see
    linked side).

    Use the notre_dame_converter instead, it works for most graphs of the page."""
    FIn = snap.TFIn(file_name)
    G4 = snap.TNGraph.Load(FIn)
    edge_list = []
    for e in G4.Edges:
        edge_list.appen(Edge('a', e.GetSrcNId(), e.GetDstNId()))
    graph = Graph(edge_list)
    return Grammar(graph, lambda x: x == 'a', lambda x: 2, lambda x: 3)
