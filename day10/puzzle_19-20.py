def parse_test_input():
    return ['[({(<(())[]>[[{[]{<()<>>',
            '[(()[<>])]({[<{<<[]>>(',
            '{([(<{}[<>[]}>{[]{[(<()>',
            '(((({<>}<{<{<>}{[]{[]{}',
            '[[<[([]))<([[{}[[()]]]',
            '[{[{({}]{}}([{[{{{}}([]',
            '{<[[]]>}<{[{[{[]{()[[[]',
            '[<(<(<(<{}))><([]([]()',
            '<{([([[(<>()){}]>(<<{{',
            '<{([{{}}[<[[[<>{}]]]>[]]']


def parse_file_input():
    with open('input.txt', 'r') as input:
        return [line.rstrip() for line in input.readlines()]


OPEN_BRACKETS = {'(', '[', '<', '{'}
CLOSING_BRACKETS = {')', ']', '>', '}'}
CLOSING_OPEN_PAIRS = {')': '(', ']': '[', '>': '<', '}': '{'}
OPEN_CLOSING_PAIRS = {'(': ')', '[': ']', '<': '>', '{': '}'}
CORRUPTED_POINTS = {')': 3, ']': 57, '}': 1197, '>': 25137}
COMPLETION_POINTS = {')': 1, ']': 2, '}': 3, '>': 4}


def get_corrupted_character(line):
    stack = []
    for character in line:
        if character in OPEN_BRACKETS:
            stack.append(character)
        elif character in CLOSING_BRACKETS:
            if not stack:
                return None

            if CLOSING_OPEN_PAIRS[character] == stack[-1]:
                stack.pop()
            else:
                return character
        else:
            raise ValueError()
    return None


def get_completion(line):
    stack = []
    for character in line:
        if character in OPEN_BRACKETS:
            stack.append(character)
        elif character in CLOSING_BRACKETS:
            if not stack:
                raise ValueError()

            if CLOSING_OPEN_PAIRS[character] == stack[-1]:
                stack.pop()
            else:
                raise ValueError()
        else:
            raise ValueError()

    completion = []
    while stack:
        character = stack.pop()
        completion.append(OPEN_CLOSING_PAIRS[character])

    return get_completion_score(completion)


def get_completion_score(completion):
    total_score = 0
    for character in completion:
        total_score = 5 * total_score + COMPLETION_POINTS[character]
    return total_score


if __name__ == '__main__':
    completion_scores = []
    for line in parse_file_input():
        corrupted_char = get_corrupted_character(line)
        if corrupted_char:
            continue
        completion_scores.append(get_completion(line))
    completion_scores.sort()
    middle_point = len(completion_scores) // 2
    print(completion_scores[middle_point])
