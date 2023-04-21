from dag import DAG, Node, Edge


if __name__ == "__main__":
    dag = DAG()
    node_a = Node(value='a')
    node_b = Node(value='b')
    node_c = Node(value='c')

    # add nodes
    dag.add_node(node=node_a)
    # dag.add_node(node=node_a)  # no exception - adding nodes is idempotent
    dag.add_node(node=node_b)
    dag.add_node(node=node_c)

    # add edges
    dag.add_edge(edge=Edge(source=node_a, target=node_b))
    # dag.add_edge(edge=Edge(node_a, node_b))  # no exception - adding edges is idempotent
    dag.add_edge(edge=Edge(source=node_b, target=node_c))
    dag.add_edge(edge=Edge(source=node_a, target=node_c))
    # dag.add_edge(edge=Edge(node_a, node_a))  # raise exception, cycle / self reference
    # dag.add_edge(edge=Edge(node_c, node_a))  # raise exception, cycle

    print(f"nodes = {len(dag.nodes)}, {list(dag.nodes)}")
    print(f"edges = {len(dag.edges)}, {list(dag.edges)}")
    print(f"get_downstream(a) = {dag.get_downstream(node_a)}")
    print(f"get_downstream(b) = {dag.get_downstream(node_b)}")
    print(f"get_downstream(c) = {dag.get_downstream(node_c)}")
    print(f"get_upstream(a) = {dag.get_upstream(node_a)}")
    print(f"get_upstream(b) = {dag.get_upstream(node_b)}")
    print(f"get_upstream(c) = {dag.get_upstream(node_c)}")
    print(f"path_exists(a, c) = {dag.path_exists(node_a, node_c)}")
    print(f"path_exists(c, a) = {dag.path_exists(node_c, node_a)}")