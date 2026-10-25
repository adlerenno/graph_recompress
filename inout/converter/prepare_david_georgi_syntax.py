"""This class is used to convert graphs, that can be read by the chess_converter to an other format used within the
bachelor thesis of David Georgi. No use in this graph compressor."""


def read(file_name, output_file):
    """ The Graph read by this function should be formatted as described in the following:
    Lines directly starting with an Hashtag are treated as comments.
    Lines directly starting with an v are vertices. They are 3 tuples: v 2 wkr (v node_id node_label).
    Lines directly starting with an d are directed edges. They are 4 tuples: d 1  2 pos (v node_id node_id edge_label).
    All other lines are ignored.
    Writes the read graph to another file with the following format.
    It's a list of numbers with the following interpretation:
    1. number of node labels.
    2. number of nodes in the graph.
    3. number of edges in the graph.
    for node in all_nodes:
        4. label of the node
        5. number of the outgoing edges of the node.
        for outgoing edge of this node:
            6. node id the outgoing edge points to.
    :param file_name: file to read from.
    :param output_file: file to write to."""
    node_outgoing_list_dict, node_label_dict, labels = {}, {}, []
    with open(file_name, 'r') as file_input:
        for line in file_input:
            if line.startswith('#'):
                continue
            elif line.startswith('d'):
                infos = line.split()
                if infos[1] in node_outgoing_list_dict:
                    node_outgoing_list_dict[infos[1]].append(infos[2])
                else:
                    node_outgoing_list_dict[infos[1]] = [infos[2]]
            elif line.startswith('v'):
                infos = line.split()
                if infos[2] not in labels:
                    labels.append(infos[2])
                node_label_dict[infos[1]] = labels.index(infos[2])+1
                node_outgoing_list_dict[infos[1]] = []
    with open(output_file, 'w') as file_output:
        file_output.write('{} {} {} '.format(len(node_label_dict.keys()), sum(len(node_outgoing_list_dict[node]) for node in node_label_dict), len(labels)))
        for node in node_label_dict.keys():
            node_outgoing_list_dict[node].sort()
            file_output.write(str(node_label_dict[node]) + ' '
                              + str(len(node_outgoing_list_dict[node])) + ' '
                              + ' '.join(node_outgoing_list_dict[node]) +
                              ('' if len(node_outgoing_list_dict[node]) == 0 else ' '))
