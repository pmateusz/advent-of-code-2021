import operator
import re
from collections import Counter

REACTION_PATTERN = re.compile(r'(?P<from>\w{2})\s->\s(?P<to>\w)')


class Problem:
    def __init__(self, pairs, reactions):
        self.pairs = pairs
        self.reactions = reactions

    def difference(self) -> int:
        counter = Counter()
        for left, right in self.pairs:
            counter[left] += 1
        counter[self.pairs[-1][1]] += 1

        most_common = max(counter.items(), key=operator.itemgetter(1))
        least_common = min(counter.items(), key=operator.itemgetter(1))

        return most_common[1] - least_common[1]

    def last_element(self):
        return self.pairs[-1][1]

    def polymer(self):
        output = []
        for pair in self.pairs:
            output.append(pair[0])
        output.append(self.last_element())
        return ''.join(output)

    def next_step(self) -> 'Problem':
        output_pairs = []
        for pair in self.pairs:
            product = self.reactions[pair]
            output_pairs.append(pair[0] + product)
            output_pairs.append(product + pair[1])

        return Problem(output_pairs, self.reactions)

    @classmethod
    def parse(cls, lines) -> 'Problem':
        def pairs(start):
            return [start[index:index + 2] for index in range(0, len(start) - 1)]

        start = lines[0]
        reactions = dict()
        for line in lines[1:]:
            match = REACTION_PATTERN.match(line)
            if match:
                from_node, to_node = match.group('from'), match.group('to')
                reactions[from_node] = to_node

        return Problem(pairs(start), reactions)


class BrokenProblem:
    def __init__(self, last_element, counter, reactions):
        self.last_element = last_element
        self.counter = counter
        self.reactions = reactions

    def difference(self):
        counter = Counter()
        for pair, number in self.counter.items():
            counter[pair[0]] += number
        counter[self.last_element] += 1

        most_common = max(counter.items(), key=operator.itemgetter(1))
        least_common = min(counter.items(), key=operator.itemgetter(1))

        return most_common[1] - least_common[1]

    def next_step(self) -> 'BrokenProblem':
        output_counter = Counter()
        for pair, number in self.counter.items():
            result = self.reactions[pair]
            output_counter[pair[0] + result] += number
            output_counter[result + pair[1]] += number

        return BrokenProblem(self.last_element, output_counter, self.reactions)

    @classmethod
    def from_problem(cls, problem: Problem):
        counter = Counter()
        for pair in problem.pairs:
            counter[pair] += 1
        return BrokenProblem(problem.pairs[-1][1], counter, problem.reactions)


def load_file_input():
    with open('input.txt', 'r') as input_stream:
        return [line.rstrip() for line in input_stream]


def load_test_input():
    return ['NNCB',
            'CH -> B',
            'HH -> N',
            'CB -> H',
            'NH -> C',
            'HB -> C',
            'HC -> B',
            'HN -> C',
            'NN -> C',
            'BH -> H',
            'NC -> B',
            'NB -> B',
            'BN -> B',
            'BB -> N',
            'BC -> B',
            'CC -> N',
            'CN -> C']


if __name__ == '__main__':
    problem = Problem.parse(load_file_input())
    broken_problem = BrokenProblem.from_problem(problem)
    print(problem.polymer())
    for step in range(1, 41):
        # print(step, problem.polymer(), problem.difference(), broken_problem.difference())
        # problem = problem.next_step()
        broken_problem = broken_problem.next_step()
    print(problem.difference(), broken_problem.difference())
