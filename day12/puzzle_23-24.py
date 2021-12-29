from collections import Counter


def parse_test_input():
    return ['dc-end',
            'HN-start',
            'start-kj',
            'dc-start',
            'dc-HN',
            'LN-dc',
            'HN-end',
            'kj-sa',
            'kj-HN',
            'kj-dc']


def parse_file_input():
    with open('input.txt', 'r') as input_file:
        return [line.rstrip() for line in input_file.readlines()]


class Path:
    def __init__(self, nodes):
        self.nodes = nodes

    def append(self, node) -> 'Path':
        new_nodes = list(self.nodes)
        new_nodes.append(node)
        return Path(new_nodes)

    def is_special_visited_twice(self, is_special):
        counter = Counter()
        for node in self.nodes:
            if is_special(node):
                counter[node] += 1
        most_common = counter.most_common(1)
        if not most_common:
            return False
        return most_common[0][1] > 1

    def tail(self):
        return self.nodes[-1]

    def __contains__(self, item):
        return item in self.nodes

    def __eq__(self, other):
        if isinstance(other, Path):
            return self.nodes == other.nodes
        return False

    def __hash__(self):
        return hash(self.nodes)

    def __str__(self):
        return self.nodes.__str__()

    def __repr__(self):
        return self.nodes.__repr__()


class Graph:
    def __init__(self, adjacency_list, source, sink, special_nodes):
        self.adjacency_list = adjacency_list
        self.source = source
        self.sink = sink
        self.special_nodes = special_nodes

    def get_paths(self):
        terminated_paths = []
        pool = [Path([self.source])]
        while pool:
            path = pool.pop()

            if self.is_terminated(path):
                terminated_paths.append(path)
                continue

            from_node = path.tail()
            from_node_adjacency_list = self.get_neighbours(from_node)
            for to_node in from_node_adjacency_list:
                if path.is_special_visited_twice(graph.is_special) and self.is_special(to_node) and to_node in path:
                    continue
                if not self.is_allowed(from_node, to_node):
                    continue
                new_path = path.append(to_node)
                pool.append(new_path)

        return terminated_paths

    def get_neighbours(self, node):
        return self.adjacency_list.get(node)

    def is_terminated(self, path: Path) -> bool:
        return path.tail() == self.sink

    def is_special(self, node: str) -> bool:
        return node in self.special_nodes

    def is_allowed(self, from_node: str, to_node: str) -> bool:
        return to_node != self.source and from_node != self.sink

    @classmethod
    def parse(cls, text) -> 'Graph':
        source, sink = 'start', 'end'
        adjacency_list = dict()

        for line in text:
            node_from, node_to = line.split('-')
            if node_from not in adjacency_list:
                adjacency_list[node_from] = set()
            if node_to not in adjacency_list:
                adjacency_list[node_to] = set()
            node_from_neighbours = adjacency_list[node_from]
            node_to_neighbours = adjacency_list[node_to]
            node_from_neighbours.add(node_to)
            node_to_neighbours.add(node_from)

        return cls(adjacency_list, source, sink,
                   {node for node in adjacency_list if node.islower() and node != source and node != sink})


if __name__ == '__main__':
    graph = Graph.parse(parse_file_input())
    paths = graph.get_paths()
    for path in paths:
        print(path)
    print(len(paths))
    print('here')
