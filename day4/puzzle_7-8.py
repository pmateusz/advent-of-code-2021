import re
import sys

WHITESPACE_PATTERN = re.compile(r'\s+')
COMMA_PATTERN = re.compile(r'[,]')


def parse_numbers(line, pattern):
    elements = [element for element in re.split(pattern, line) if len(element) > 0]
    return list(map(int, elements))


class Tile:

    def __init__(self, number):
        self.number = number
        self.is_marked = False


class Board:

    def __init__(self, numbers):
        self.rows = [[Tile(number) for number in row] for row in numbers]

    def mark(self, number):
        for row in self.rows:
            for tile in row:
                if tile.number == number:
                    tile.is_marked = True

    def get_row(self, row_number):
        return self.rows[row_number]

    def get_column(self, column_number):
        return [row[column_number] for row in self.rows]

    def is_winner(self):
        board_size = len(self.rows)
        for row_number in range(0, board_size):
            if all(tile.is_marked for tile in self.get_row(row_number)):
                return True

        for column_number in range(0, board_size):
            if all(tile.is_marked for tile in self.get_column(column_number)):
                return True
        return False

    def sum_unmarked(self):
        unmarked = 0

        for row in self.rows:
            for tile in row:
                if not tile.is_marked:
                    unmarked += tile.number

        return unmarked


def load_input():
    with open('input.txt', 'r') as input:
        raw_values = input.readlines()

    raw_bingo_numbers = raw_values[0]
    raw_bingo_numbers = raw_bingo_numbers.rstrip()
    bingo_numbers = parse_numbers(raw_bingo_numbers, COMMA_PATTERN)

    boards = []
    raw_board = []
    for row_index in range(2, len(raw_values)):
        line = raw_values[row_index].rstrip()
        if not line:
            boards.append(Board(raw_board))
            raw_board = []
            continue
        numbers = parse_numbers(line, WHITESPACE_PATTERN)
        raw_board.append(numbers)
    if raw_board:
        boards.append(Board(raw_board))

    return bingo_numbers, boards


if __name__ == '__main__':
    bingo_numbers, boards = load_input()

    current_round = boards
    for bingo_number in bingo_numbers:
        next_round = []
        for board in boards:
            board.mark(bingo_number)
            if not board.is_winner():
                next_round.append(board)
        if not next_round:
            print(current_round[0].sum_unmarked() * bingo_number)
            break
        current_round = next_round
