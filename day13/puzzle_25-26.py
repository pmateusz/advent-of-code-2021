import re
import os

COORDINATES_PATTERN = re.compile(r'(?P<row>\d+),(?P<column>\d+)')
FOLD_PATTERN = re.compile(r'fold\salong\s(?P<coordinate>[xy])=(?P<offset>\d+)')


class Configuration:
    def __init__(self, points, folds):
        self.points = points
        self.folds = folds

    def num_rows(self):
        return max(point[1] for point in self.points) + 1

    def num_cols(self):
        return max(point[0] for point in self.points) + 1

    def can_fold(self):
        return len(self.folds) > 0

    def fold(self):
        style, offset = self.folds[0]
        if style == 'x':
            return self.__fold_column(offset)
        elif style == 'y':
            return self.__fold_row(offset)

    def __fold_row(self, fold_row):
        adjusted_points = []
        for c, r in self.points:
            if r < fold_row:
                adjusted_points.append((c, r))
            else:
                bottom_distance = r - fold_row
                adjusted_points.append((c, fold_row - bottom_distance))

        unique_points = set(adjusted_points)
        return Configuration(unique_points, self.folds[1:])

    def __fold_column(self, fold_column):
        adjusted_points = []
        for c, r in self.points:
            if c < fold_column:
                adjusted_points.append((c, r))
            else:
                right_distance = c - fold_column
                adjusted_points.append((fold_column - right_distance, r))

        unique_points = set(adjusted_points)
        return Configuration(unique_points, self.folds[1:])

    def __str__(self):
        board = [['.' for _ in range(0, self.num_cols())] for _ in range(0, self.num_rows())]

        for c, r in self.points:
            board[r][c] = '#'

        return os.linesep.join(''.join(row) for row in board)

    def __len__(self):
        return len(self.points)


class Parser:

    def __init__(self):
        pass

    def parse(self, lines):
        mesh = []
        folds = []
        for line in lines:
            match = COORDINATES_PATTERN.match(line)
            if match:
                row, column = int(match.group('row')), int(match.group('column'))
                mesh.append((row, column))
                continue

            match = FOLD_PATTERN.match(line)
            if match:
                coordinate, offset = match.group('coordinate'), int(match.group('offset'))
                folds.append((coordinate, offset))
        return Configuration(mesh, folds)


def load_test_input():
    return ['6,10',
            '0,14',
            '9,10',
            '0,3',
            '10,4',
            '4,11',
            '6,0',
            '6,12',
            '4,1',
            '0,13',
            '10,12',
            '3,4',
            '3,0',
            '8,4',
            '1,10',
            '2,14',
            '8,10',
            '9,0',
            'fold along y=7',
            'fold along x=5']


def load_file_input():
    with open('input.txt', 'r') as input_stream:
        output_lines = []
        for line in input_stream:
            line = line.rstrip()
            if line:
                output_lines.append(line)
        return output_lines


if __name__ == '__main__':
    lines = load_file_input()
    parser = Parser()
    configuration = parser.parse(lines)

    while configuration.can_fold():
        configuration = configuration.fold()

    print(configuration)
