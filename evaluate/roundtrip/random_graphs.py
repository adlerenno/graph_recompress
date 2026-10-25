from evaluate import timetest
from evaluate.timetest import log
from evaluate.timetest.average import log_average_times
from evaluate.timetest.normal import timing
from inout.input.random_graph_generator import random_grammar
from recompress import recompress, decompress

"""Use this class to test random generated graphs."""


def random_test(vertex_count=10000, edge_count=50000, labels=None):
    """Creates a random graph with the given characteristics.
    :returns size of the compressed graph and the size of the graph before it was compressed."""
    if labels is None:
        labels = ['a', 'b', 'c']
    grammar = random_grammar(vertex_count, edge_count, edge_count//5, labels, {label: 2 for label in labels})
    begin_size = grammar.size_of_hole_grammar()
    recompress(grammar)
    min_size = grammar.size_of_hole_grammar()
    decompress(grammar)
    decompressed_size = grammar.size_of_hole_grammar()
    return min_size, begin_size, decompressed_size


@timing
def systematic_test(vertex_count=5000, edge_count=25000, labels=('a', 'b', 'c'), graph_count=10):
    """Tests multiple random graphs with the same characteristics.
    :param vertex_count: number of nodes in the graph.
    :param edge_count: number of edges of the graph. They will be all normal edges.
    :param labels: an iterable of labels for edges.
    :param graph_count: number of graphs, that should be tested.
    :returns the average compression ratio of all these graphs."""
    begin_size, min_size, decom_size = [], [], []
    for i in range(graph_count):
        mini, begin, decom = random_test(vertex_count=vertex_count, edge_count=edge_count, labels=labels)
        begin_size.append(begin)
        min_size.append(mini)
        decom_size.append(decom)

    minimal_size = min(min_size)
    maximal_size = max(min_size)
    sum_size = sum(min_size)
    average_size = sum_size / len(min_size)
    sigma_size = (sum((size-average_size)**2 for size in min_size)/len(min_size))**(1/2)
    average_ratio = sum_size/sum(decom_size)
    minimal_ratio = minimal_size/decom_size[0]
    maximal_ratio = maximal_size/decom_size[0]
    distance = min(maximal_ratio - average_ratio, average_ratio - minimal_ratio)
    sigma_ratio = (sum((size/decom_size[0]-average_ratio)**2 for size in min_size)/len(min_size))**(1/2)

    # print results
    log_average_times()
    log('Average Size: {}.'.format(average_size))
    log('Minimum Size: {}.'.format(minimal_size))
    log('Maximum Size: {}.'.format(maximal_size))
    log('Average Ratio: {}.'.format(average_ratio))
    log('Sigma: {}.'.format(sigma_size))
    log('Minimum: {}.'.format(minimal_ratio))
    log('Maximum: {}.'.format(maximal_ratio))
    log('Max Distance from average: {}.'.format(distance))
    log('Sigma: {}.'.format(sigma_ratio))
    return average_ratio, begin_size, min_size, decom_size


def systematic_random_graph_test():
    """Tests complete sets of characteristics and write them to a file"""
    file = open('../../../Testgraphen/results/results_random.txt', 'w')
    data_file = open('../../../Testgraphen/results/results_data_random.txt', 'w')
    data_file.write('# Edge Count, Vertex Count, Begin size, Recompressed Size, Decompressed Size')
    for edge_count in (50, 100, 200, 500, 1000, 2000, 5000, 10000):
        for vertex_count in (50, 100, 200, 500, 1000, 2000, 5000, 10000):
            for labels in (['a'],):
                #timetest.log_file = open('results/random_{}_{}_{}.txt'.format(edge_count, vertex_count, ''.join(labels)), 'w')
                average_ratio, begin_size, min_size, decom_size= systematic_test(edge_count=edge_count,
                                                vertex_count=vertex_count,
                                                labels=labels,
                                                graph_count=10 if edge_count >= 5000 else 20
                                                )
                #timetest.log_file.close()
                file.write(f'{edge_count} {vertex_count} {average_ratio}\n')
                file.flush()
                for begin, mini, decom in zip(begin_size, min_size, decom_size):
                    data_file.write(f'{edge_count} {vertex_count} {begin} {mini} {decom}\n')
                data_file.flush()
    file.close()
    data_file.close()


def random_graph_to_real_graph_test():
    """Tests complete sets of characteristics and write them to files"""
    for vertex_count, edge_count, name in ((4038, 88234, 'facebook-combined'),
                                           (7115, 103689, 'Wiki-Vote'),
                                           (18772, 396160, 'CA-CondMat'),
                                           (62586, 147892, 'p2p-Gnutella31'),
                                           (34546, 421578, 'Cit-HepPh'),
                                           (36692, 367662, 'Email-Enron'),
                                           (403394, 3387388, 'amazon0601'),
                                           (875713, 5105039, 'web-google'),
                                           (325729, 1497134, 'web-NotreDame'),
                                           (334863, 925872, 'com-amazon'),
                                           (265214, 420045, 'Email-EuAll'),
                                           (1134890, 2987624, 'com-youtube'),
                                           (1965206, 5533214, 'roadNet-CA'),
                                           (1088092, 3083796, 'roadNet-PA'),
                                           (1379917, 3843320, 'roadNet-TX'),
                                           (2394385, 5021410, 'WikiTalk')):
        timetest.log_file = open('results/random_real_{}_{}_{}_a.txt'.format(name, edge_count, vertex_count), 'w')
        systematic_test(edge_count=edge_count,
                        vertex_count=vertex_count,
                        labels=('a',),
                        graph_count=1
                        )
        timetest.log_file.close()
