import operator


def parse_input():
    # return [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]
    with open('input.txt') as input:
        return list(map(int, input.readline().split(',')))


def absolute_distance(positions, center):
    return sum(abs(center - position) for position in positions)


def momentum_distance(positions, center):
    return sum(abs(center - position) * (abs(center - position) + 1) / 2 for position in positions)


if __name__ == '__main__':
    positions = parse_input()
    min_pos, max_pos = min(positions), max(positions)
    values = [(center, momentum_distance(positions, center)) for center in range(min_pos, max_pos + 1, 1)]
    print(min(values, key=operator.itemgetter(1))[1])
