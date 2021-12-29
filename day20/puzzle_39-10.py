import os


class Algorithm:
    def __init__(self, config):
        self.vector = config

    def __getitem__(self, item):
        return self.vector[item]


class Image:
    def __init__(self, matrix, field_outside='.'):
        self.matrix = None
        self.num_rows = None
        self.num_cols = None
        self.field_outside = field_outside
        self.update_matrix(matrix)

    def __copy_matrix(self):
        return [list(row) for row in self.matrix]

    def copy(self):
        matrix_copy = self.__copy_matrix()
        return Image(matrix_copy, self.field_outside)

    def update_matrix(self, matrix):
        self.matrix = matrix
        self.num_rows = len(self.matrix)
        self.num_cols = len(self.matrix[0])

    def enhance_matrix(self, algorithm):
        matrix_copy = self.__copy_matrix()

        for row in range(0, self.num_rows):
            for col in range(0, self.num_cols):
                number = self.get_number(row, col)
                pixel = algorithm[number]
                matrix_copy[row][col] = pixel

        self.update_matrix(matrix_copy)

    def has_active_frame(self, algorithm) -> bool:
        frame_points = set()
        for col in range(-1, self.num_cols + 1):
            frame_points.add((-1, col))
            frame_points.add((self.num_rows, col))
        for row in range(-1, self.num_rows + 1):
            frame_points.add((row, -1))
            frame_points.add((self.num_rows, -1))
        for row, col in frame_points:
            if algorithm[self.get_number(row, col)] == '#':
                return True
        return False

    def append_frame(self):
        framed_matrix = [[self.field_outside] * (self.num_cols + 2) for _ in range(self.num_rows + 2)]
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                framed_matrix[row + 1][col + 1] = self.matrix[row][col]
        self.update_matrix(framed_matrix)

    def enhance(self, algorithm: Algorithm) -> 'Image':
        image_copy = self.copy()
        for _ in range(3):
            image_copy.append_frame()

        image_copy.enhance_matrix(algorithm)

        if self.field_outside == '.':
            image_copy.field_outside = algorithm[0]
        else:
            image_copy.field_outside = algorithm[-1]
        return image_copy

    def get_number(self, row, col):
        number = 0
        raw_number = []
        for row_offset in range(-1, 2):
            for col_offset in range(-1, 2):
                pixel = self.get_pixel(row + row_offset, col + col_offset)
                if pixel == 0:
                    raw_number.append('0')
                else:
                    raw_number.append('1')
                number <<= 1
                number |= pixel
        parsed_number = int(''.join(raw_number), 2)
        assert parsed_number == number
        return number

    def get_pixel(self, row, col) -> int:
        if 0 <= row < self.num_rows and 0 <= col < self.num_cols:
            if self.matrix[row][col] == '#':
                return 1
            else:
                return 0
        else:
            if self.field_outside == '#':
                return 1
            return 0

    def __str__(self):
        return os.linesep.join([''.join(row) for row in self.matrix])

    def lit_pixels(self) -> int:
        number = 0
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if self.matrix[row][col] == '#':
                    number += 1
        return number


def read_test_input():
    algorithm = Algorithm(
        '..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#')
    image = Image([['#', '.', '.', '#', '.'],
                   ['#', '.', '.', '.', '.'],
                   ['#', '#', '.', '.', '#'],
                   ['.', '.', '#', '.', '.'],
                   ['.', '.', '#', '#', '#']])
    current_image = image
    for _ in range(50):
        current_image = current_image.enhance(algorithm)
    print(current_image)
    print(current_image.lit_pixels())
    # .enhance(algorithm).lit_pixels())


def read_file_input():
    with open('input.txt', 'r') as input_stream:
        lines = [line.rstrip() for line in input_stream.readlines()]
        algorithm = Algorithm(lines[0])
        image_matrix = [list(line) for line in lines[2:]]
        image = Image(image_matrix)
        current_image = image
        for _ in range(50):
            current_image = current_image.enhance(algorithm)
        print(current_image)
        print(current_image.lit_pixels())


if __name__ == '__main__':
    read_file_input()
