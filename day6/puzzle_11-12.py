from typing import List


class FishCounter:

    def __init__(self, state=8):
        self.state = state

    def next_step(self) -> bool:
        if self.state <= 0:
            self.state = 6
            return True
        self.state -= 1
        return False


def parse_input() -> List[FishCounter]:
    # return [FishCounter(state) for state in [3, 4, 3, 1, 2]]
    with open('input.txt', 'r') as input:
        return [int(raw_number) for raw_number in input.readline().split(',')]


def bottom_up(inital_state, days):
    total_dict = {}

    def inner_bottom_up(day, growth):
        state = (day, growth)
        if state in total_dict:
            return total_dict[state]

        next_day = day + growth + 1
        if next_day <= days:
            total = inner_bottom_up(next_day, 6) + inner_bottom_up(next_day, 8)
        else:
            total = 1
        total_dict[state] = total
        return total

    result = sum(inner_bottom_up(0, growth) for growth in inital_state)
    return result


if __name__ == '__main__':
    print(bottom_up(parse_input(), 256))

    # fish = parse_input()
    # for day in range(1, 257):
    #     print(day)
    #     for sample in list(fish):
    #         if sample.next_step():
    #             fish.append(FishCounter())
    #     # print(f'Day {day}: {",".join([str(sample.state) for sample in fish])}')
    # print(len(fish))
