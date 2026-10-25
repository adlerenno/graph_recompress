from classes import *


def read(file_name):
    """ The Graph read by this function should be formatted as described in the following:
    Lines directly starting with an Hashtag are treated as comments.
    Lines directly starting with an v are vertices. They are 3 tuples: v 2 wkr (v node_id node_label).
    Lines directly starting with an d are directed edges. They are 4 tuples: d 1  2 pos (v node_id node_id edge_label).
    All other lines are ignored.
    :returns a graph object, even if the file is not readable. """
    edge_list = []
    edge_label_dict, node_label_dict = {}, {}
    with open(file_name, 'r') as file_input:
        for line in file_input:
            if line.startswith('#'):
                continue
            elif line.startswith('d'):
                infos = line.split()
                edge_list.append(Edge(infos[3], infos[1], infos[2]))
                edge_label_dict[infos[3]] = 2
            elif line.startswith('v'):
                infos = line.split()
                edge_list.append(Edge(infos[2], infos[1]))
                node_label_dict[infos[2]] = 1
    for key in node_label_dict.keys():
        if key in edge_label_dict:
            raise KeyError(key)
    # print('node_label_count: {}, edge_label_count: {}'.format(len(node_label_dict.keys()), len(edge_label_dict.keys())))
    edge_label_dict.update(node_label_dict)
    graph = Graph(edge_list)
    return Grammar(graph, lambda x: x in edge_label_dict, lambda x: edge_label_dict[x], lambda x: edge_label_dict[x]+1)


def read_comments(file_name):
    """Read the lines with an hashtag of a file."""
    comments = []
    with open(file_name, 'r') as file_input:
        for line in file_input:
            if line.startswith("#"):
                comments.append(line)
    return "".join(comments)
