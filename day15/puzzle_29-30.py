import heapq
import os


def load_file_input():
    with open('input.txt', 'r') as input_file:
        return [line.rstrip() for line in input_file]


def load_test_input():
    return ['1163751742',
            '1381373672',
            '2136511328',
            '3694931569',
            '7463417111',
            '1319128137',
            '1359912421',
            '3125421639',
            '1293138521',
            '2311944581']


class Path:
    def __init__(self, moves, risk):
        self.moves = moves
        self.risk = risk

    def append(self, move, move_risk):
        moves = list(self.moves)
        moves.append(move)
        risk = self.risk + move_risk
        return Path(moves, risk)

    def __contains__(self, item):
        return item in self.moves

    def __lt__(self, other):
        if isinstance(other, Path):
            return self.risk < other.risk or (self.risk == other.risk and len(self.moves) < len(other.moves))
        return False

    def tail(self):
        return self.moves[-1]


class Board:

    def __init__(self, board):
        self.board = board
        self.num_rows = len(self.board)
        self.num_cols = len(self.board[0])

    def get_neighbours(self, point):
        row, col = point
        neighbours = []
        for off in [-1, 1]:
            neighbours.append((row + off, col))
            neighbours.append((row, col + off))

        return [(row, col) for row, col in neighbours if 0 <= row < self.num_rows and 0 <= col < self.num_cols]

    def h_stack(self, other):
        copy_board = [list(row) for row in self.board]
        for row in range(self.num_rows):
            copy_board[row].extend(other.board[row])
        return Board(copy_board)

    def v_stack(self, other):
        copy_board = [list(row) for row in self.board]
        for row in range(other.num_rows):
            copy_board.append(other.board[row])
        return Board(copy_board)

    def shift(self):
        shifted_board = [[Board.shift_number(number) for number in row] for row in self.board]
        return Board(shifted_board)

    def get_risk(self, move):
        row, col = move
        return self.board[row][col]

    @staticmethod
    def shift_number(number):
        next_number = number + 1
        if next_number < 10:
            return next_number
        return 1

    def __str__(self):
        return Board.__matrix_to_str(self.board, 1)

    @staticmethod
    def __matrix_to_str(matrix, offset):
        return os.linesep.join([''.join([f'{number:{offset}d}' for number in row]) for row in matrix])

    def get_neighbours(self, point):
        r, c = point
        neighbours = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
        return [(r, c) for r, c in neighbours if 0 <= r < self.num_rows and 0 <= c < self.num_cols]

    def get_restricted_parent(self, point):
        r, c = point
        neighbours = [(r - 1, c), (r, c - 1)]
        return [(r, c) for r, c in neighbours if 0 <= r < self.num_rows and 0 <= c < self.num_cols]

    def get_dijkstra_path(self):
        max_value = max([max(row) for row in self.board])
        max_cost_path = self.num_cols * self.num_rows * max_value

        class Node:

            def __init__(self, point, distance, prev):
                self.point = point
                self.distance = distance
                self.prev = prev
                self.active = True

            def __lt__(self, other):
                return self.distance < other.distance

            def __str__(self):
                return f'{self.point}, distance: {self.distance}'

        heap = []
        point_to_node = dict()
        for row in range(self.num_rows - 1, -1, -1):
            for col in range(self.num_cols - 1, -1, -1):
                point = (row, col)
                point_to_node[point] = Node(point, max_cost_path, None)
        point_to_node[(0, 0)].distance = 0
        for node in point_to_node.values():
            heap.append(node)
        heapq.heapify(heap)

        while heap:
            node = heapq.heappop(heap)
            if not node.active:
                continue

            for neighbour_point in self.get_neighbours(node.point):
                neighbour_node = point_to_node[neighbour_point]
                alternative_distance = node.distance + self.board[neighbour_point[0]][neighbour_point[1]]
                if neighbour_node.distance > alternative_distance:
                    neighbour_node.active = False
                    new_node = Node(neighbour_point, alternative_distance, node.point)
                    point_to_node[new_node.point] = new_node
                    heapq.heappush(heap, new_node)

        path = []
        point = (self.num_rows - 1, self.num_cols - 1)

        while point is not None:
            path.append(point)
            point = point_to_node[point].prev
        path.reverse()

        total_cost = 0
        for point in path[1:]:
            total_cost += self.board[point[0]][point[1]]

        return total_cost

    def get_low_cost_path(self):
        max_value = max([max(row) for row in self.board])
        max_cost_path = self.num_cols * self.num_rows * max_value
        cost_matrix = [[max_cost_path for _ in range(0, self.num_cols)] for _ in range(0, self.num_rows)]
        last_row = self.num_rows - 1
        last_col = self.num_cols - 1
        cost_matrix[last_row][last_col] = self.board[last_row][last_col]

        # last_row
        for col in range(last_col - 1, -1, -1):
            cost_matrix[last_row][col] = cost_matrix[last_row][col + 1] + self.board[last_row][col]

        # last_col
        for row in range(last_row - 1, -1, -1):
            cost_matrix[row][last_col] = cost_matrix[row + 1][last_col] + self.board[row][last_col]

        # other rows and columns
        for row in range(last_row - 1, -1, -1):
            for col in range(last_col - 1, -1, -1):
                min_cost = min(cost_matrix[row + 1][col], cost_matrix[row][col + 1])
                cost_matrix[row][col] = min_cost + self.board[row][col]

        recovered_path = []
        current_point = (0, 0)
        recovered_path.append(current_point)
        while current_point != (last_row, last_col):
            row, col = current_point
            if row == last_row:
                current_point = (row, col + 1)
            elif col == last_col:
                current_point = (row + 1, col)
            else:
                if cost_matrix[row][col + 1] < cost_matrix[row + 1][col]:
                    current_point = (row, col + 1)
                else:
                    current_point = (row + 1, col)
            recovered_path.append(current_point)

        total_cost = 0
        for point in recovered_path[1:]:
            total_cost += self.board[point[0]][point[1]]

        total_cost_ref = cost_matrix[0][0] - self.board[0][0]

        return cost_matrix[0][0] - self.board[0][0]

    @classmethod
    def parse(cls, lines):
        matrix = [[int(raw_number) for raw_number in line] for line in lines]
        return Board(matrix)


if __name__ == '__main__':
    initial_board = Board.parse(load_file_input())
    print(initial_board.get_dijkstra_path())
    print(initial_board.get_low_cost_path())
    row_board = initial_board
    full_board = None
    for _ in range(5):
        current_board = row_board
        working_board = row_board
        for _ in range(4):
            current_board = current_board.shift()
            working_board = working_board.h_stack(current_board)
        if full_board is None:
            full_board = working_board
        else:
            full_board = full_board.v_stack(working_board)
        row_board = row_board.shift()
    print(full_board)
    print(full_board.get_low_cost_path())
    print(full_board.get_dijkstra_path())
