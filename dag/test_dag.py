from dag import DAG, Node, Edge
import unittest


class Testing(unittest.TestCase):
    # TODO convert to hypothesis / property based testing
    def test_add_node_a(self):
        dag = DAG()
        node_a = Node(value='a')
        self.assertTrue(len(dag.nodes) == 0)
        self.assertTrue(node_a not in dag.nodes)

        dag.add_node(node=node_a)
        self.assertTrue(len(dag.nodes) == 1)
        self.assertTrue(node_a in dag.nodes)

    def test_add_node_ab(self):
        dag = DAG()
        node_a = Node(value='a')
        node_b = Node(value='b')

        dag.add_node(node=node_a)
        dag.add_node(node=node_b)
        self.assertTrue(len(dag.nodes) == 2)
        self.assertTrue(node_a in dag.nodes)
        self.assertTrue(node_b in dag.nodes)

    def test_add_node_idempotency(self):
        dag = DAG()
        node_a = Node(value='a')

        dag.add_node(node=node_a)
        dag.add_node(node=node_a)  # if same node is added again, it can be ignored
        self.assertTrue(len(dag.nodes) == 1)
        self.assertTrue(node_a in dag.nodes)

    def test_add_edge_ab(self):
        dag = DAG()
        node_a = Node(value='a')
        node_b = Node(value='b')
        dag.add_node(node=node_a)
        dag.add_node(node=node_b)
        edge_ab = Edge(source=node_a, target=node_b)
        # a -> b
        dag.add_edge(edge=edge_ab)
        self.assertTrue(len(dag.edges) == 1)
        self.assertTrue(edge_ab in dag.edges)

    def test_add_edge_idempotency(self):
        dag = DAG()
        node_a = Node(value='a')
        node_b = Node(value='b')
        dag.add_node(node=node_a)
        dag.add_node(node=node_b)
        edge_ab = Edge(source=node_a, target=node_b)
        # a -> b
        dag.add_edge(edge=edge_ab)
        dag.add_edge(edge=edge_ab)
        self.assertTrue(len(dag.edges) == 1)
        self.assertTrue(edge_ab in dag.edges)

    def test_add_edge_cycle_aa(self):
        dag = DAG()
        node_a = Node(value='a')
        dag.add_node(node=node_a)
        # a -> a
        edge_aa = Edge(source=node_a, target=node_a)
        self.assertRaises(Exception, lambda: dag.add_edge(edge=edge_aa))

    def test_add_edge_cycle_aba(self):
        dag = DAG()
        node_a = Node(value='a')
        node_b = Node(value='b')
        dag.add_node(node=node_a)
        dag.add_node(node=node_b)

        # a -> b -> a
        edge_ab = Edge(source=node_a, target=node_b)
        edge_ba = Edge(source=node_b, target=node_a)

        dag.add_edge(edge=edge_ab)
        self.assertRaises(Exception, lambda: dag.add_edge(edge=edge_ba))

    def test_add_edge_cycle_abca(self):
        dag = DAG()
        node_a = Node(value='a')
        node_b = Node(value='b')
        node_c = Node(value='c')
        dag.add_node(node=node_a)
        dag.add_node(node=node_b)
        dag.add_node(node=node_c)

        # a -> b -> c -> a
        edge_ab = Edge(source=node_a, target=node_b)
        edge_bc = Edge(source=node_b, target=node_c)
        edge_ca = Edge(source=node_c, target=node_a)
        dag.add_edge(edge=edge_ab)
        dag.add_edge(edge=edge_bc)
        self.assertRaises(Exception, lambda: dag.add_edge(edge=edge_ca))

    def test_get_downstream_empty(self):
        dag = DAG()
        node_a = Node(value='a')
        self.assertTrue(dag.get_downstream(node_a) == [])

    def test_get_upstream_empty(self):
        dag = DAG()
        node_a = Node(value='a')
        self.assertTrue(dag.get_upstream(node_a) == [])

    def test_get_downstream_ab(self):
        dag = DAG()
        node_a = Node(value='a')
        node_b = Node(value='b')
        dag.add_node(node_a)
        dag.add_node(node_b)

        # a -> b
        edge_ab = Edge(source=node_a, target=node_b)
        dag.add_edge(edge=edge_ab)
        self.assertTrue(dag.get_downstream(node_a) == [node_b])
        self.assertTrue(dag.get_downstream(node_b) == [])

    def test_get_upstream_ab(self):
        dag = DAG()
        node_a = Node(value='a')
        node_b = Node(value='b')
        dag.add_node(node_a)
        dag.add_node(node_b)

        # a -> b
        edge_ab = Edge(source=node_a, target=node_b)
        dag.add_edge(edge=edge_ab)
        self.assertTrue(dag.get_upstream(node_a) == [])
        self.assertTrue(dag.get_upstream(node_b) == [node_a])

    def test_get_downstream_ab_ac(self):
        dag = DAG()
        node_a = Node(value='a')
        node_b = Node(value='b')
        node_c = Node(value='c')
        dag.add_node(node_a)
        dag.add_node(node_b)
        dag.add_node(node_c)

        # a -> b, a -> c
        edge_ab = Edge(source=node_a, target=node_b)
        edge_ac = Edge(source=node_a, target=node_c)
        dag.add_edge(edge=edge_ab)
        dag.add_edge(edge=edge_ac)

        self.assertTrue(sorted(dag.get_downstream(node_a)) == sorted([node_b, node_c]))
        self.assertTrue(dag.get_downstream(node_b) == [])
        self.assertTrue(dag.get_downstream(node_c) == [])

    def test_get_upstream_ab_ac(self):
        dag = DAG()
        node_a = Node(value='a')
        node_b = Node(value='b')
        node_c = Node(value='c')
        dag.add_node(node_a)
        dag.add_node(node_b)
        dag.add_node(node_c)

        # a -> b, a -> c
        edge_ab = Edge(source=node_a, target=node_b)
        edge_ac = Edge(source=node_a, target=node_c)
        dag.add_edge(edge=edge_ab)
        dag.add_edge(edge=edge_ac)

        self.assertTrue(dag.get_upstream(node_a) == [])
        self.assertTrue(dag.get_upstream(node_b) == [node_a])
        self.assertTrue(dag.get_upstream(node_c) == [node_a])

    def test_get_downstream_abc(self):
        dag = DAG()
        node_a = Node(value='a')
        node_b = Node(value='b')
        node_c = Node(value='c')
        dag.add_node(node_a)
        dag.add_node(node_b)
        dag.add_node(node_c)

        # a -> b -> c
        edge_ab = Edge(source=node_a, target=node_b)
        edge_bc = Edge(source=node_b, target=node_c)
        dag.add_edge(edge=edge_ab)
        dag.add_edge(edge=edge_bc)
        self.assertTrue(dag.get_downstream(node_a) == [node_b])
        self.assertTrue(dag.get_downstream(node_b) == [node_c])
        self.assertTrue(dag.get_downstream(node_c) == [])

    def test_get_upstream_abc(self):
        dag = DAG()
        node_a = Node(value='a')
        node_b = Node(value='b')
        node_c = Node(value='c')
        dag.add_node(node_a)
        dag.add_node(node_b)
        dag.add_node(node_c)

        # a -> b -> c
        edge_ab = Edge(source=node_a, target=node_b)
        edge_bc = Edge(source=node_b, target=node_c)
        dag.add_edge(edge=edge_ab)
        dag.add_edge(edge=edge_bc)
        self.assertTrue(dag.get_upstream(node_a) == [])
        self.assertTrue(dag.get_upstream(node_b) == [node_a])
        self.assertTrue(dag.get_upstream(node_c) == [node_b])

    def test_path_exists_ab(self):
        dag = DAG()
        node_a = Node(value='a')
        node_b = Node(value='b')
        dag.add_node(node=node_a)
        dag.add_node(node=node_b)
        self.assertFalse(dag.path_exists(source=node_a, target=node_b))
        # a -> b
        edge_ab = Edge(source=node_a, target=node_b)
        dag.add_edge(edge_ab)
        self.assertTrue(dag.path_exists(source=node_a, target=node_b))
        self.assertFalse(dag.path_exists(source=node_b, target=node_a))

    def test_path_exists_abc(self):
        dag = DAG()
        node_a = Node(value='a')
        node_b = Node(value='b')
        node_c = Node(value='c')
        dag.add_node(node=node_a)
        dag.add_node(node=node_b)
        dag.add_node(node=node_c)
        self.assertFalse(dag.path_exists(source=node_a, target=node_c))
        # a -> b -> c
        edge_ab = Edge(source=node_a, target=node_b)
        edge_bc = Edge(source=node_b, target=node_c)
        dag.add_edge(edge_ab)
        dag.add_edge(edge_bc)
        self.assertTrue(dag.path_exists(source=node_a, target=node_c))
        self.assertTrue(dag.path_exists(source=node_a, target=node_b))
        self.assertTrue(dag.path_exists(source=node_b, target=node_c))
        self.assertFalse(dag.path_exists(source=node_c, target=node_a))


if __name__ == '__main__':
    unittest.main()