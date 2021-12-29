import os
from typing import List


class Board:

    def __init__(self, board: List[List[str]]):
        self.board = board
        self.num_rows = len(self.board)
        self.num_cols = len(self.board[0])
        self.right_movers = list()
        self.down_movers = list()
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                element = self.board[row][col]
                pos = row, col
                if element == '>':
                    self.right_movers.append(pos)
                elif element == 'v':
                    self.down_movers.append(pos)
                else:
                    assert element == '.'

    def next(self) -> 'Board':
        working_board = self.__create_empty()
        for pos in self.right_movers:
            next_pos = self.__next_right_pos(pos)
            if self[next_pos] == '.':
                working_board[next_pos] = '>'
            else:
                working_board[pos] = '>'
        for pos in self.down_movers:
            next_pos = self.__next_down_pos(pos)
            if working_board[next_pos] == '.' and self[next_pos] != 'v':
                working_board[next_pos] = 'v'
            else:
                working_board[pos] = 'v'
        return working_board

    def __getitem__(self, item):
        row, col = item
        return self.board[row][col]

    def __setitem__(self, pos, value):
        assert value == '>' or value == 'v'
        row, col = pos
        assert self.board[row][col] == '.'
        self.board[row][col] = value
        if value == '>':
            self.right_movers.append(pos)
        else:
            self.down_movers.append(pos)

    def __create_empty(self) -> 'Board':
        board = [['.'] * self.num_cols for _ in range(0, self.num_rows)]
        return Board(board)

    def __next_right_pos(self, pos):
        row, col = pos
        return row, (col + 1) % self.num_cols

    def __next_down_pos(self, pos):
        row, col = pos
        return (row + 1) % self.num_rows, col

    def __str__(self):
        lines = []
        for row in self.board:
            lines.append(''.join(row))
        return os.linesep.join(lines)

    def __eq__(self, other):
        if isinstance(other, Board):
            return self.board == other.board
        return False

    def __hash__(self):
        return hash(self.board)

    @classmethod
    def from_text(cls, lines: List[str]):
        rows = []
        for line in lines:
            row = list(line)
            rows.append(row)
        return cls(rows)


def create_text_example():
    return Board.from_text(['v...>>.vv>',
                            '.vv>>.vv..',
                            '>>.>v>...v',
                            '>>v>>.>.v.',
                            'v>v.vv.v..',
                            '>.>>..v...',
                            '.vv..>.>v.',
                            'v.v..>>v.v',
                            '....v..v.>'])


def create_puzzle_example():
    with open('input.txt', 'r') as file_stream:
        board = [line.rstrip() for line in file_stream]
        return Board.from_text(board)


if __name__ == '__main__':
    board = Board.from_text(['...>>>>>...'])
    print(board)
    print(board.next())
    print(board.next().next())
    print()

    other_board = Board.from_text(['..........', '.>v....v..', '.......>..', '..........'])
    print(other_board)
    print()
    print(other_board.next())

    some_other_board = Board.from_text(['...>...',
                                        '.......',
                                        '......>',
                                        'v.....>',
                                        '......>',
                                        '.......',
                                        '..vvv..'])
    print(some_other_board)
    print()
    print(some_other_board.next())
    print()
    print(some_other_board.next().next())
    print()
    print(some_other_board.next().next().next())
    print()
    print(some_other_board.next().next().next().next())

    step = 0
    current_board = create_puzzle_example()
    while True:
        step += 1
        next_board = current_board.next()
        if current_board == next_board:
            break
        current_board = next_board
    print(step)
