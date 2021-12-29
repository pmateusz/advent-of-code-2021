class Node:

    def visit(self, visitor):
        pass


class InnerNode(Node):
    def __init__(self, left, right):
        super(InnerNode, self).__init__()

        self.left = left
        self.right = right

    def __str__(self):
        left_str = self.left.__str__()
        right_str = self.right.__str__()
        return f'[{left_str}, {right_str}]'

    def visit(self, visitor):
        visitor.on_enter(self)

        self.left.visit(visitor)
        self.right.visit(visitor)

        visitor.on_exit(self)

    def magnitude(self):
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()

    def copy(self):
        left_node = self.left.copy()
        right_node = self.right.copy()
        return InnerNode(left_node, right_node)


class LeafNode(Node):
    def __init__(self, value):
        super(LeafNode, self).__init__()

        self.value = value

    def __str__(self):
        return str(self.value)

    def visit(self, visitor):
        visitor.on_enter(self)
        visitor.on_exit(self)

    def magnitude(self):
        return self.value

    def copy(self):
        return LeafNode(self.value)


class ExplodeVisitor:
    def __init__(self):
        self.triggered = False
        self.depth = []

    def on_enter(self, node):
        if self.triggered:
            return

        self.depth.append(node)
        if len(self.depth) > 4 and isinstance(node, InnerNode):
            assert isinstance(node.left, LeafNode)
            assert isinstance(node.right, LeafNode)

            zero_node = LeafNode(0)
            parent = self.depth[-2]
            if parent.left == node:
                parent.left = zero_node
            else:
                parent.right = zero_node
            self.depth.pop()
            self.depth.append(zero_node)

            path = list(self.depth)
            right_regular = self.find_next_regular(path)
            if right_regular:
                right_regular.value += node.right.value

            left_regular = self.find_prev_regular(path)
            if left_regular:
                left_regular.value += node.left.value

            self.triggered = True

    def on_exit(self, node):
        if self.triggered:
            return

        self.depth.pop()

    def find_prev_regular(self, path):
        path_to_use = list(path)

        if len(path_to_use) == 1:
            return None

        # move up to the tree following left branches
        node = path_to_use.pop()
        parent = path_to_use.pop()
        while parent.left == node:
            node = parent
            if not path_to_use:
                return None

            parent = path_to_use.pop()

        node = parent.left
        # find first regular following right branches
        while isinstance(node, InnerNode):
            node = node.right
        return node

    def find_next_regular(self, path):
        path_to_use = list(path)

        if len(path_to_use) == 1:
            return None

        # move up to the tree following right branches
        node = path_to_use.pop()
        parent = path_to_use.pop()
        while parent.right == node:
            node = parent
            if not path_to_use:
                return None

            parent = path_to_use.pop()

        node = parent.right
        # find first regular following left branches
        while isinstance(node, InnerNode):
            node = node.left
        return node


class SplitVisitor:
    def __init__(self):
        self.triggered = False
        self.depth = list()

    def on_enter(self, node):
        if self.triggered:
            return

        self.depth.append(node)

        if isinstance(node, LeafNode):
            if node.value >= 10:
                self.depth.pop()
                parent = self.depth[-1]

                left_value = node.value // 2
                right_value = node.value - left_value
                split_node = InnerNode(LeafNode(left_value), LeafNode(right_value))
                if parent.left == node:
                    parent.left = split_node
                else:
                    parent.right = split_node
                self.triggered = True

    def on_exit(self, node):
        if self.triggered:
            return

        self.depth.pop()


class Tree:

    def __init__(self, node: Node):
        self.node = node

    def copy(self):
        return Tree(self.node.copy())

    def add(self, tree: 'Tree') -> 'Tree':
        node = InnerNode(self.node.copy(), tree.node.copy())
        tree = Tree(node)
        while True:
            explode_visitor = ExplodeVisitor()
            node.visit(explode_visitor)
            if explode_visitor.triggered:
                continue
            else:
                split_visitor = SplitVisitor()
                node.visit(split_visitor)
                if split_visitor.triggered:
                    continue
                return tree

    def __str__(self):
        return self.node.__str__()

    @classmethod
    def parse(cls, expression):
        node = cls.parse_node(expression)
        return cls(node)

    @classmethod
    def parse_node(cls, exp):
        if isinstance(exp, int):
            return LeafNode(exp)
        left_node, right_node = cls.parse_node(exp[0]), Tree.parse_node(exp[1])
        return InnerNode(left_node, right_node)


if __name__ == '__main__':
    numbers = [[1, 1],
               [2, 2],
               [3, 3],
               [4, 4],
               [5, 5],
               [6, 6]]

    numbers_larger_example = [
        [[[0, [4, 5]], [0, 0]], [[[4, 5], [2, 6]], [9, 5]]],
        [7, [[[3, 7], [4, 3]], [[6, 3], [8, 8]]]],
        [[2, [[0, 8], [3, 4]]], [[[6, 7], 1], [7, [1, 6]]]],
        [[[[2, 4], 7], [6, [0, 5]]], [[[6, 8], [2, 8]], [[2, 1], [4, 5]]]],
        [7, [5, [[3, 8], [1, 4]]]],
        [[2, [2, 2]], [8, [8, 1]]],
        [2, 9],
        [1, [[[9, 3], 9], [[9, 0], [0, 7]]]],
        [[[5, [7, 4]], 7], 1],
        [[[[4, 2], 2], 6], [8, 7]]
    ]

    with open('input.txt', 'r') as input:
        numbers_puzzle = [eval(line.rstrip()) for line in input]

    trees = [Tree.parse(number) for number in numbers_puzzle]
    tree = trees[0]
    magnitues = []
    for left_pos in range(0, len(trees)):
        for right_pos in range(left_pos + 1, len(trees)):
            left_tree = trees[left_pos]
            right_tree = trees[right_pos]
            magnitues.append(left_tree.add(right_tree).node.magnitude())
            magnitues.append(right_tree.add(left_tree).node.magnitude())

    print(max(magnitues))