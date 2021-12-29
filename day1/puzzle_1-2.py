def num_increased(values):
    counter = 0
    for right in range(1, len(values)):
        left = right - 1
        if values[left] < values[right]:
            counter += 1
    return counter


def parse_input():
    with open('input.txt', 'r') as input:
        return [int(line.rstrip()) for line in input.readlines()]


def get_windows(values):
    return [values[index] + values[index + 1] + values[index + 2] for index in range(0, (len(values) // 3) * 3)]


if __name__ == '__main__':
    values = parse_input()
    print(num_increased(values))
    print(num_increased(get_windows(values)))
