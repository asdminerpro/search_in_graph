from generators import (
    RandomGraphGenerator,
    CompleteGraphGenerator,
    WorstForLevitGenerator,
    BestForFordBellmanGraphGenerator,
    WorstForFordBellmanGraphGenerator,
    UndirectedConnectedRandomGraphGenerator
)

from algorithms import (
    Dijkstra,
    FordBellman,
    Levit,
    MinimalPathBetweenSpecifiedVertexes,
    INF
)

from time_manager import timer
from graph import Graph
import time
import unittest


def init_graph():
    g = Graph()
    g.add_edge(0, 1, 2)
    g.add_edge(3, 4, 1)
    g.add_edge(3, 2, 0)
    g.add_edge(6, 4, 111)
    g.add_edge(2, 15, 5)
    g.add_edge(1, 0, 5)
    return g


def init_generator(generator, count_vertex, count_edges, seed=0):
    return generator(count_vertex, count_edges)(seed)


class GraphTests(unittest.TestCase):
    def test_add_edge(self):
        g = Graph()
        g.add_edge(0, 1, 1)
        self.assertEqual(len(g.adjacency_list), 2)
        g.add_edge(1000, 14, -10)
        self.assertEqual(len(g.adjacency_list), 1001)

    def test_count_vertex(self):
        g = init_graph()
        self.assertEqual(g.count_vertex(), 7)
        g.add_edge(11, 12, 1)
        self.assertEqual(g.count_vertex(), 9)

    def test_count_edges(self):
        g = init_graph()
        self.assertEqual(g.count_edges(), 6)
        g.add_edge(100, 123, -100)
        self.assertEqual(g.count_edges(), 7)

    def test_adjacent_vertex(self):
        g = init_graph()
        self.assertEqual(g.adjacent_vertex(0), [[1, 2]])
        self.assertEqual(g.adjacent_vertex(3), [[4, 1], [2, 0]])
        self.assertEqual(g.adjacent_vertex(6), [[4, 111]])
        self.assertEqual(g.adjacent_vertex(2), [[15, 5]])
        self.assertEqual(g.adjacent_vertex(1), [[0, 5]])
        g.add_edge(3, 100, -1)
        self.assertEqual(g.adjacent_vertex(3), [[4, 1], [2, 0], [100, -1]])

    def test_save_graph(self):
        g = Graph()
        g.add_edge(0, 1)
        g.add_edge(0, 2, 2)
        with open('test_graph.txt', 'w') as graph:
            g.save(graph)

        with open('test_graph.txt', 'r') as graph:
            read_graph = graph.read()
        self.assertEqual(read_graph, str(g))

    def test_read_graph(self):
        g = Graph()
        with open('test_graph.txt', 'r') as graph:
            g.read(graph)
        self.assertEqual('0 1 1\n0 2 2', str(g))


class DijkstraTest(unittest.TestCase):
    def test_pathfinder(self):
        min_path = Dijkstra(init_graph())
        self.assertEqual(min_path.pathfinder(0, 1), 2)
        self.assertEqual(min_path.pathfinder(1, 0), 5)
        self.assertEqual(min_path.pathfinder(3, 15), 5)
        self.assertEqual(min_path.pathfinder(3, 12), INF)
        self.assertEqual(min_path.pathfinder(0), [0, 2] +
                         [INF for _ in range(14)])

    def test_applicability_of_these_graph(self):
        g = init_graph()
        self.assertEqual(Dijkstra(g).applicability_of_these_graph(), True)
        g = Graph()
        g.add_edge(0, 1, -1)
        self.assertEqual(Dijkstra(g).applicability_of_these_graph(), False)


class FordBellmanTest(unittest.TestCase):
    def test_pathfinder(self):
        g = init_graph()
        p = FordBellman(g)
        self.assertEqual(p.pathfinder(0, 1), 2)
        self.assertEqual(FordBellman(g).pathfinder(1, 0), 5)
        self.assertEqual(FordBellman(g).pathfinder(3, 15), 5)
        self.assertEqual(FordBellman(g).pathfinder(3, 12), INF)
        self.assertEqual(FordBellman(g).pathfinder(0), [0, 2] +
                         [INF for _ in range(14)])

    def test_applicability_of_these_graph(self):
        g = init_graph()
        self.assertEqual(FordBellman(g).applicability_of_these_graph(),
                         True)
        g = Graph()
        g.add_edge(0, 1, -1)
        self.assertEqual(FordBellman(g).applicability_of_these_graph(),
                         True)
        g.add_edge(1, 2, 1)
        g.add_edge(2, 0, -1)
        self.assertEqual(FordBellman(g).applicability_of_these_graph(),
                         False)


class LevitTest(unittest.TestCase):
    def test_pathfinder(self):
        g = init_graph()
        p = FordBellman(g)
        self.assertEqual(p.pathfinder(0, 1), 2)
        self.assertEqual(Levit(g).pathfinder(0), [0, 2] +
                         [INF for _ in range(14)])
        self.assertEqual(Levit(g).pathfinder(1, 0), 5)
        self.assertEqual(Levit(g).pathfinder(3, 15), 5)
        self.assertEqual(Levit(g).pathfinder(3, 12), INF)

    def test_applicability_of_these_graph(self):
        g = init_graph()
        self.assertEqual(Levit(g).applicability_of_these_graph(), True)
        g = Graph()
        g.add_edge(0, 1, -1)
        self.assertEqual(Levit(g).applicability_of_these_graph(), True)
        g.add_edge(1, 2, 1)
        g.add_edge(2, 0, -1)
        self.assertEqual(FordBellman(g).applicability_of_these_graph(),
                         False)


class GenerateRandomGraphTest(unittest.TestCase):
    def test_size_graph(self):
        g = init_generator(RandomGraphGenerator, 4, 4, 2)
        self.assertEqual(g.count_edges(), 4)
        self.assertEqual(g.count_vertex(), 4)
        self.assertEqual(g.max_vertex(), 3)

    def test_determinate(self):
        g = init_generator(RandomGraphGenerator, 4, 4, 2)
        self.assertEqual(Dijkstra(g).pathfinder(0, 2), 855)
        self.assertEqual(Dijkstra(g).pathfinder(0), [0, INF, 855, INF])


class GenerateCompleteGraphTest(unittest.TestCase):
    def test_size_graph(self):
        g = init_generator(CompleteGraphGenerator, 4, 6, 2)
        self.assertEqual(g.count_edges(), 4 * 3)
        self.assertEqual(g.count_vertex(), 4)
        self.assertEqual(g.max_vertex(), 3)

    def test_determinate(self):
        g = init_generator(CompleteGraphGenerator, 4, 6, 2)
        self.assertEqual(Dijkstra(g).pathfinder(0, 2), 883)
        self.assertEqual(Dijkstra(g).pathfinder(0),
                         [0, 978, 883, 970])


class GenerateBestForFordBellmanGraphTest(unittest.TestCase):
    def test_size_graph(self):
        g = init_generator(BestForFordBellmanGraphGenerator, 4, 4, 2)
        self.assertEqual(g.count_edges(), 4)
        self.assertEqual(g.count_vertex(), 4)
        self.assertEqual(g.max_vertex(), 3)

    def test_determinate(self):
        g = init_generator(BestForFordBellmanGraphGenerator, 6, 7, 2)
        self.assertEqual(Dijkstra(g).pathfinder(0, 2), 0)
        self.assertEqual(Dijkstra(g).pathfinder(0),
                         [0, 0, 0, 0, 0, 0])


class GenerateWorstForFordBellmanGraphTest(unittest.TestCase):
    def test_size_graph(self):
        g = init_generator(WorstForFordBellmanGraphGenerator, 5, 6, 2)
        self.assertEqual(g.count_edges(), 6)
        self.assertEqual(g.count_vertex(), 5)
        self.assertEqual(g.max_vertex(), 4)

    def test_determinate(self):
        g = init_generator(WorstForFordBellmanGraphGenerator, 6, 7, 2)
        self.assertEqual(Dijkstra(g).pathfinder(0, 2), 1861)
        self.assertEqual(Dijkstra(g).pathfinder(0),
                         [0, 978, 1861, 2831, 3700, 3757])


class GenerateWorstForLevitGraphTest(unittest.TestCase):
    def test_size_graph(self):
        g = init_generator(WorstForLevitGenerator, 5, 10)
        self.assertEqual(g.count_edges(), 20)
        self.assertEqual(g.count_vertex(), 5)
        self.assertEqual(g.max_vertex(), 4)

    def test_determinate(self):
        g = init_generator(WorstForLevitGenerator, 6, 15)
        self.assertEqual(Dijkstra(g).pathfinder(0, 2), 0)
        self.assertEqual(Dijkstra(g).pathfinder(0), [0, 0, 0, 0, 0, 0])


class GenerateUndirectedConnectedRandomGraphTest(unittest.TestCase):
    def test_size_graph(self):
        g = init_generator(UndirectedConnectedRandomGraphGenerator, 5, 10)
        self.assertEqual(g.count_edges(), 10)
        self.assertEqual(g.count_vertex(), 5)
        self.assertEqual(g.max_vertex(), 4)

    def test_determinate(self):
        generator = UndirectedConnectedRandomGraphGenerator(6, 15)
        g = generator()
        self.assertEqual(Dijkstra(g).pathfinder(0, 2), 1186)
        self.assertEqual(Dijkstra(g).pathfinder(0),
                         [0, 654, 1186, 553, 288, 722])


class MinimalPathBetweenSpecifiedVertexesTest(unittest.TestCase):
    def test_prim(self):
        g = init_graph()
        edges = g.edge_list.copy()
        for edge in edges:
            g.add_edge(edge.f, edge.s, edge.weight)
        pathfinder = MinimalPathBetweenSpecifiedVertexes(g, [2, 3, 4, 6])
        self.assertEqual(pathfinder.get_min_path(), 112)
        pathfinder.specified_vertexes = [2, 3, 4]
        self.assertEqual(pathfinder.get_min_path(), 1)
        pathfinder.specified_vertexes = [1, 2, 3, 4, 5]
        self.assertGreaterEqual(pathfinder.get_min_path(), INF)

    def test_get_graph_from_specified_vertexes(self):
        g = init_graph()
        pathfinder = MinimalPathBetweenSpecifiedVertexes(g, [2, 3, 4])
        self.assertEqual(len(pathfinder.get_graph_from_specified_vertexes()),
                         3)
        self.assertEqual(pathfinder.get_graph_from_specified_vertexes(),
                         [[INF, INF, INF], [0, INF, 1], [INF, INF, INF]])

    def test_floyd(self):
        g = Graph()
        g.add_edge(0, 1)
        g.add_edge(1, 2)
        g.add_edge(0, 2)
        pathfinder = MinimalPathBetweenSpecifiedVertexes(g, [0])
        self.assertEqual(pathfinder.floyd_algorithm(),
                         [[INF, 1, 1], [INF, INF, 1], [INF, INF, INF]])
        g.add_edge(1, 0)
        pathfinder = MinimalPathBetweenSpecifiedVertexes(g, [0])
        self.assertEqual(pathfinder.floyd_algorithm(),
                         [[2, 1, 1], [1, 2, 1], [INF, INF, INF]])


class TimeManagerTest(unittest.TestCase):
    def test_generate_best_and_worst_ford_bellman(self):
        generator = BestForFordBellmanGraphGenerator(1000, 5000)
        g = generator()
        t1, a, b = timer(FordBellman(g))

        generator = WorstForFordBellmanGraphGenerator(1000, 5000)
        g = generator()
        t2, a, b = timer(FordBellman(g))
        self.assertGreater(t1, -t2)

    def test_generate_worst_and_random_levit(self):
        generator = CompleteGraphGenerator(100, 4950)
        g = generator()
        t1, a, b = timer(Levit(g))

        generator = WorstForLevitGenerator(100, 4950)
        g = generator()
        t2, a, b = timer(Levit(g))

        self.assertGreater(t2, t1)


if __name__ == '__main__':
    unittest.main()
