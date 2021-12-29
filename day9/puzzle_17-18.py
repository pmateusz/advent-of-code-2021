def parse_test_input():
    return [[2, 1, 9, 9, 9, 4, 3, 2, 1, 0],
            [3, 9, 8, 7, 8, 9, 4, 9, 2, 1],
            [9, 8, 5, 6, 7, 8, 9, 8, 9, 2],
            [8, 7, 6, 7, 8, 9, 6, 7, 8, 9],
            [9, 8, 9, 9, 9, 6, 5, 6, 7, 8]]


def parse_file_input():
    board = []
    with open('input.txt', 'r') as input:
        for line in input.readlines():
            line = line.rstrip()
            board.append([int(raw_digit) for raw_digit in line])
    return board


def get_dim(board):
    return len(board), len(board[0])


def get_neighbours(point, dim):
    row, col = point
    num_rows, num_cols = dim
    return [(r, c) for r, c in [(row, col + 1), (row + 1, col), (row - 1, col), (row, col - 1)]
            if r < num_rows and r >= 0 and c < num_cols and c >= 0]


def get_low_points(board):
    dim = get_dim(board)
    num_rows, num_cols = dim

    low_points = []
    for pr in range(0, num_rows):
        for pc in range(0, num_cols):
            neighbours = get_neighbours((pr, pc), (num_rows, num_cols))
            if all(board[nr][nc] > board[pr][pc] for nr, nc in neighbours):
                low_points.append((pr, pc))

    return low_points


def get_basin_size(board, point):
    dim = get_dim(board)
    to_visit = [point]
    visited = set()

    basin_size = 0
    while to_visit:
        p = to_visit.pop()

        if p in visited:
            continue

        basin_size += 1
        visited.add(p)
        for np in get_neighbours(p, dim):
            if np in visited:
                continue

            nr, nc = np
            if board[nr][nc] == 9:
                continue

            to_visit.append(np)
    return basin_size


def get_basin_sizes(board):
    return [get_basin_size(board, lp) for lp in get_low_points(board)]


if __name__ == '__main__':
    basin_sizes = get_basin_sizes(parse_file_input())
    basin_sizes.sort(reverse=True)
    print(basin_sizes[0] * basin_sizes[1] * basin_sizes[2])
