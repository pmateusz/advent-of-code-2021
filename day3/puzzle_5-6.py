import operator
from collections import Counter


def load_input():
    with open('input.txt', 'r') as input:
        values = []
        for raw_line in input:
            line = raw_line.rstrip()
            row = [int(line[index]) for index in range(0, len(line))]
            values.append(row)
        return values


def load_test_input():
    return [[0, 0, 1, 0, 0],
            [1, 1, 1, 1, 0],
            [1, 0, 1, 1, 0],
            [1, 0, 1, 1, 1],
            [1, 0, 1, 0, 1],
            [0, 1, 1, 1, 1],
            [0, 0, 1, 1, 1],
            [1, 1, 1, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 1, 0, 0, 1],
            [0, 0, 0, 1, 0],
            [0, 1, 0, 1, 0]]


def puzzle_5():
    values = load_input()
    num_positions = len(values[0])
    counters = []
    for position in range(0, num_positions):
        counter = Counter()
        for row in values:
            current_bit = row[position]
            counter[current_bit] += 1
        counters.append(counter)

    gamma = 0
    epsilon = 0
    for counter in counters:
        most_common_value = counter.most_common(1)[0][0]
        gamma <<= 1
        gamma += most_common_value

        least_common_value = 1 - most_common_value
        epsilon <<= 1
        epsilon += least_common_value

    print(gamma * epsilon)


def row_to_bin(row):
    value = 0
    for bit in row:
        value <<= 1
        value += bit
    return value


def get_bit(values, position, filter_criteria, tie_breaker):
    counter = Counter()
    for row in values:
        counter[row[position]] += 1
    if counter[0] == counter[1]:
        return tie_breaker
    return filter_criteria(counter, key=counter.get)


def filter_value(values, filter_criteria, tie_breaker):
    num_positions = len(values[0])
    filtered_values = values
    for pos in range(0, num_positions):
        if len(filtered_values) <= 1:
            break
        bit = get_bit(filtered_values, pos, filter_criteria, tie_breaker)
        filtered_values = [row for row in filtered_values if row[pos] == bit]
    return row_to_bin(filtered_values[0])


if __name__ == '__main__':
    values = load_input()
    oxygen_gen = filter_value(values, max, 1)
    co2_scrubber = filter_value(values, min, 0)
    print(oxygen_gen, co2_scrubber, oxygen_gen * co2_scrubber)
