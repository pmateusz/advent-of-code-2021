from enum import Enum


class Direction(Enum):
    FORWARD = 1
    UP = 2
    DOWN = 3

    @classmethod
    def parse(cls, value):
        if value not in STR_TO_DIRECTION:
            raise ValueError(value)
        return STR_TO_DIRECTION[value]


STR_TO_DIRECTION = {'forward': Direction.FORWARD, 'up': Direction.UP, 'down': Direction.DOWN}


def load_input():
    with open('input.txt', 'r') as input:
        values = []
        for raw_line in input.readlines():
            line = raw_line.rstrip()
            raw_direction, raw_value = line.split(' ')
            direction, value = Direction.parse(raw_direction), int(raw_value)
            values.append((direction, value))
        return values


def puzzle3():
    movements = load_input()
    horizontal_pos, vertical_pos = 0, 0
    for direction, value in movements:
        if direction == Direction.DOWN:
            vertical_pos = vertical_pos + value
        elif direction == Direction.UP:
            vertical_pos = max(vertical_pos - value, 0)
        elif direction == Direction.FORWARD:
            horizontal_pos += value
    print(horizontal_pos * vertical_pos)


def puzzle4():
    movements = load_input()
    horizontal_pos, vertical_pos, aim = 0, 0, 0
    for direction, value in movements:
        if direction == Direction.DOWN:
            aim = aim + value
        elif direction == Direction.UP:
            aim = max(aim - value, 0)
        elif direction == Direction.FORWARD:
            horizontal_pos += value
            vertical_pos += aim * value
    print(horizontal_pos * vertical_pos)


if __name__ == '__main__':
    puzzle4()
