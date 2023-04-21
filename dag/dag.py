from dataclasses import dataclass, field


@dataclass(unsafe_hash=True, order=True)
class Node:
    value: any


@dataclass(unsafe_hash=True, order=True)
class Edge:
    source: Node
    target: Node


@dataclass(unsafe_hash=True, order=True)
class DAG:
    nodes: set[Node] = field(default_factory=set)
    edges: set[Edge] = field(default_factory=set)

    def add_node(self, node: Node) -> None:
        self.nodes.add(node)

    def add_edge(self, edge: Edge) -> None:
        source = edge.source
        target = edge.target
        # check nodes are members of the graph
        if source not in self.nodes:
            raise Exception(f"\"{source}\" is not added to graph")
        if target not in self.nodes:
            raise Exception(f"\"{target}\" is not added to graph")

        # check for cycles
        # if source + target are the same
        if source == target:
            raise Exception(f"\"{source}\" cannot have an edge to itself")
        # if path from target to source, then adding edge would create a cycle
        if self.path_exists(source=target, target=source):
            raise Exception(f"Adding edge \"{source}->{target}\" would create a cycle")

        # otherwise, there are no cycles, we can add the edge
        self.edges.add(edge)

    def get_downstream(self, node: Node) -> list[Node]:
        nodes = []
        for x in self.edges:
            if x.source == node:
                # node -> sample_database.sql
                nodes.append(x.target)
        nodes.sort()
        return nodes

    def get_upstream(self, node: Node) -> list[Node]:
        nodes = []
        for x in self.edges:
            if x.target == node:
                # sample_database.sql -> node
                nodes.append(x.source)
        nodes.sort()
        return nodes

    def path_exists(self, source: Node, target: Node) -> bool:
        return self.__depth_first_search(source, target, visited=[])

    def __depth_first_search(self, source: Node, target: Node, visited=None) -> bool:
        # do recursive DFS from source to target
        if visited is None:
            visited = []
        for x in self.get_downstream(source):
            if x not in visited:
                visited.append(x)
                self.__depth_first_search(source=x, target=target, visited=visited)
        return target in visited
