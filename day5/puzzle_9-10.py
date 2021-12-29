import re
import logging
from collections import Counter
from typing import Tuple, List

LINE_PATTERN = re.compile(r'(?P<x1>\d+),(?P<y1>\d+)\s+->\s+(?P<x2>\d+),(?P<y2>\d+)')


class LineSegment:

    def __init__(self, p1: Tuple[int, int], p2: Tuple[int, int]):
        self.p1 = p1
        self.p2 = p2

    def get_grid_points(self) -> List[Tuple[int, int]]:
        x1, y1 = self.p1
        x2, y2 = self.p2
        begin_x, end_x = (x1, x2) if x1 < x2 else (x2, x1)

        if begin_x == end_x:
            begin_y, end_y = (y1, y2) if y1 < y2 else (y2, y1)
            return [(begin_x, y) for y in range(begin_y, end_y + 1, 1)]

        a = float(y2 - y1) / float(x2 - x1)
        b = y1 - a * x1
        points = []
        for x in range(begin_x, end_x + 1, 1):
            y = a * x + b
            if int(y) == y:
                points.append((int(x), int(y)))
        return points

    def is_vertical(self) -> bool:
        return self.p1[0] == self.p2[0]

    def is_horizontal(self) -> bool:
        return self.p1[1] == self.p2[1]


def parse_input() -> List[LineSegment]:
    line_segments = []
    with open('input.txt', 'r') as input:
        for line in input.readlines():
            match = LINE_PATTERN.match(line)
            if match:
                x1, y1, x2, y2 = [int(match.group(name)) for name in ['x1', 'y1', 'x2', 'y2']]
                line_segment = LineSegment((x1, y1), (x2, y2))
                line_segments.append(line_segment)
            else:
                logging.error('Failed to match %s', line)
    return line_segments


def puzzle9(line_segments: List[LineSegment]) -> int:
    counter = Counter()
    for line_segment in line_segments:
        if line_segment.is_horizontal() or line_segment.is_vertical():
            points = line_segment.get_grid_points()
            for point in points:
                counter[point] += 1

    total_points = 0
    for point, freq in counter.items():
        if freq > 1:
            total_points += 1
    return total_points


def puzzle10(line_segments: List[LineSegment]) -> int:
    counter = Counter()
    for line_segment in line_segments:
        points = line_segment.get_grid_points()
        for point in points:
            counter[point] += 1

    total_points = 0
    for point, freq in counter.items():
        if freq > 1:
            total_points += 1
    return total_points


if __name__ == '__main__':
    line_segments = parse_input()
    print(puzzle10(line_segments))
