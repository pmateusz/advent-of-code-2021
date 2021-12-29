from collections import Counter
from typing import List, Optional


class Pattern:

    def __init__(self, pattern: str):
        self.pattern = pattern
        self.raw_pattern = set(list(pattern))

    def __len__(self):
        return len(self.pattern)

    def __str__(self):
        return self.pattern.__str__()

    def __repr__(self):
        return self.pattern.__repr__()

    def __eq__(self, other):
        if not isinstance(other, Pattern):
            return False

        return self.raw_pattern == other.raw_pattern

    def __contains__(self, item):
        if not isinstance(item, Pattern):
            return False
        return self.raw_pattern.issuperset(item.raw_pattern)

    def __hash__(self):
        return hash(self.raw_pattern)

    def join(self, other: 'Pattern') -> 'Pattern':
        pattern = ''.join(self.raw_pattern.union(other.raw_pattern))
        return Pattern(pattern)

    @classmethod
    def parse(cls, text: str) -> 'Pattern':
        return cls(text)


class Solution:

    def __init__(self):
        self.patterns = dict()

    def set(self, digit: int, pattern: Pattern):
        self.patterns[digit] = pattern

    def get(self, digit: int) -> Pattern:
        return self.patterns.get(digit)

    def get_digit(self, pattern: Pattern) -> Optional[int]:
        for digit in self.patterns:
            if self.patterns[digit] == pattern:
                return digit
        return None

    def __contains__(self, item):
        return item in self.patterns.values()


def get_test_input():
    return ['be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe',
            'edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc',
            'fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg',
            'fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb',
            'aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea',
            'fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb',
            'dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe',
            'bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef',
            'egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb',
            'gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce']


def get_input():
    with open('input.txt', 'r') as input:
        return input.readlines()


def parse_line(line: str):
    return [Pattern.parse(pattern) for pattern in line.split(' ')]


def find_by_length(patterns, length) -> List[Pattern]:
    return [pattern for pattern in patterns if len(pattern) == length]


def find_by_length_assert_one(patterns, length) -> Pattern:
    filtered = find_by_length(patterns, length)
    assert len(filtered) == 1
    return filtered[0]


def find_one(patterns) -> Pattern:
    return find_by_length_assert_one(patterns, 2)


def find_eight(patterns) -> Pattern:
    return find_by_length_assert_one(patterns, 7)


def find_four(patterns) -> Pattern:
    return find_by_length_assert_one(patterns, 4)


def find_seven(patterns) -> Pattern:
    return find_by_length_assert_one(patterns, 3)


def find_nine(patterns, solution) -> Pattern:
    four = solution.get(4)
    seven = solution.get(7)
    seven_and_four = four.join(seven)
    filtered_patterns = [pattern for pattern in patterns if pattern not in solution and seven_and_four in pattern]
    assert len(filtered_patterns) == 1
    return filtered_patterns[0]


def find_zero(patterns, solution) -> Pattern:
    one = solution.get(1)
    filtered_patterns = [pattern for pattern in find_by_length(patterns, 6)
                         if one in pattern and pattern not in solution]
    assert len(filtered_patterns) == 1
    return filtered_patterns[0]


def find_six(patterns, solution) -> Pattern:
    filtered_patterns = [pattern for pattern in find_by_length(patterns, 6)
                         if pattern not in solution]
    assert len(filtered_patterns) == 1
    return filtered_patterns[0]


def find_five(patterns, solution) -> Pattern:
    six = solution.get(6)
    filtered_patterns = [pattern for pattern in find_by_length(patterns, 5) if pattern in six]
    assert len(filtered_patterns) == 1
    return filtered_patterns[0]


def find_three(patterns, solution) -> Pattern:
    one = solution.get(1)
    filtered_patterns = [pattern for pattern in find_by_length(patterns, 5) if one in pattern]
    assert len(filtered_patterns) == 1
    return filtered_patterns[0]


def find_two(patterns, solution) -> Pattern:
    filtered_patterns = [pattern for pattern in find_by_length(patterns, 5) if pattern not in solution]
    assert len(filtered_patterns) == 1
    return filtered_patterns[0]


def decode(line: str):
    line = line.rstrip()
    left, right = line.split(' | ')
    left_patterns = parse_line(left)
    right_patterns = parse_line(right)

    solution = Solution()
    solution.set(1, find_one(left_patterns))
    solution.set(8, find_eight(left_patterns))
    solution.set(4, find_four(left_patterns))
    solution.set(7, find_seven(left_patterns))
    solution.set(9, find_nine(left_patterns, solution))
    solution.set(0, find_zero(left_patterns, solution))
    solution.set(6, find_six(left_patterns, solution))
    solution.set(5, find_five(left_patterns, solution))
    solution.set(3, find_three(left_patterns, solution))
    solution.set(2, find_two(left_patterns, solution))

    return int(''.join([str(solution.get_digit(pattern)) for pattern in right_patterns]))


if __name__ == '__main__':
    length_counter = Counter()
    print(sum(decode(line) for line in get_input()))
