from generators import (
    RandomGraphGenerator,
    CompleteGraphGenerator,
    WorstForLevitGenerator,
    BestForFordBellmanGraphGenerator,
    WorstForFordBellmanGraphGenerator,
    UndirectedConnectedRandomGraphGenerator
)
import argparse


GENERATORS = {
    'random': RandomGraphGenerator,
    'complete': CompleteGraphGenerator,
    'best for ford-bellman': BestForFordBellmanGraphGenerator,
    'worst for ford-bellman': WorstForFordBellmanGraphGenerator,
    'worst for levit': WorstForLevitGenerator,
    'connected random graph': UndirectedConnectedRandomGraphGenerator
}


def parseargs():
    description = '''
                Generate graph
                Possible generators name
                1. random
                2. complete
                3. best for ford-bellman
                4. worst for ford-bellman
                5. worst for levit
                6. connected random graph
                '''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-e', action='store', dest='count_edges',
                        type=int)
    parser.add_argument('-v', action='store', dest='count_vertex',
                        type=int)
    parser.add_argument('-gn', action='store', dest='name_generator',
                        choices=['random',
                                 'complete',
                                 'best for ford-bellman',
                                 'worst for ford-bellman',
                                 'worst for levit',
                                 'connected random graph'
                                 ],
                        type=str, default='random')
    parser.add_argument('-fn', action='store', dest='filename',
                        type=str, default='stdout',
                        help='file name where to save generated graph')
    parser.add_argument('-s', action='store', dest='seed',
                        default=0, type=int)

    return parser.parse_args()


def generate(arguments):
    generator = GENERATORS[arguments.name_generator](arguments.count_vertex,
                                                     arguments.count_edges)
    graph = generator(arguments.seed)
    if arguments.filename == 'stdout':
        print(str(graph))
    else:
        with open(arguments.filename, 'w') as file:
            graph.save(file)


if __name__ == '__main__':
    generate(parseargs())