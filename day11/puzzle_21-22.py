import os


def parse_test_input():
    return [list(map(int, line))
            for line in ['5483143223',
                         '2745854711',
                         '5264556173',
                         '6141336146',
                         '6357385478',
                         '4167524645',
                         '2176841721',
                         '6882881134',
                         '4846848554',
                         '5283751526']]


def parse_file_input():
    with open('input.txt', 'r') as input:
        return [list(map(int, line.rstrip())) for line in input.readlines()]


class Board:

    def __init__(self, board):
        self.board = board
        self.num_rows = len(self.board)
        self.num_cols = len(self.board[0]) if self.num_rows > 0 else 0

    def count_flashes(self):
        flashes = 0
        for row in range(0, self.num_rows):
            for col in range(0, self.num_cols):
                if self.board[row][col] == 0:
                    flashes += 1
        return flashes

    def next_step(self):
        next_step_board = [[number + 1 for number in row] for row in self.board]

        fired = set()
        queue = [(row, col) for row in range(0, self.num_rows) for col in range(0, self.num_cols) if
                 next_step_board[row][col] > 9]
        while queue:
            point = queue.pop()
            if point in fired:
                raise ValueError()
            fired.add(point)
            for adjacent_point in self.get_adjacent_nodes(point):
                if adjacent_point in fired:
                    continue
                a_r, a_c = adjacent_point
                next_step_board[a_r][a_c] += 1
                if next_step_board[a_r][a_c] == 10 and adjacent_point not in fired:
                    queue.append(adjacent_point)

        return Board([[number if number <= 9 else 0 for number in row] for row in next_step_board])

    def get_adjacent_nodes(self, point):
        neighbours = []
        row, col = point
        for shift_row in range(-1, 2):
            for shift_col in range(-1, 2):
                new_row = row + shift_row
                new_col = col + shift_col
                if 0 <= new_row < self.num_rows and 0 <= new_col < self.num_cols and (
                        new_row != row or new_col != col):
                    neighbours.append((new_row, new_col))
        return neighbours

    def __str__(self):
        return os.linesep.join(''.join(map(str, row)) for row in self.board)

    @classmethod
    def parse(cls, board):
        return cls(board)


if __name__ == '__main__':
    raw_input = parse_file_input()
    current_board = Board.parse(raw_input)
    print('Before any steps:')
    print(current_board)
    total_flashes = current_board.count_flashes()
    for step in range(1, 1000):
        print()
        print('After step ', step)
        current_board = current_board.next_step()
        print(current_board)
        local_flashes = current_board.count_flashes()
        if local_flashes == current_board.num_cols * current_board.num_rows:
            print(step)
            break
        total_flashes += local_flashes
    print(total_flashes)
