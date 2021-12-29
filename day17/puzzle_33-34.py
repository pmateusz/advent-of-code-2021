class State:

    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def get_acceleration(self):
        d_x = 1 if self.velocity[0] > 0 else -1
        d_y = -1
        return d_x, d_y

    def get_next_velocity(self):
        v_x, v_y = self.velocity
        nv_x, n_vy = v_x, v_y - 1
        if v_x > 0:
            nv_x -= 1
        elif v_x < 0:
            nv_x += 1
        return nv_x, n_vy

    def get_next_position(self):
        v_x, v_y = self.velocity
        x, y = self.position
        return x + v_x, y + v_y

    def next(self):
        return State(self.get_next_position(), self.get_next_velocity())

    def __str__(self):
        return f'{self.position} {self.velocity}'


class Area:

    def __init__(self, min_x, max_x, min_y, max_y):
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

    def __contains__(self, point) -> bool:
        x, y = point
        return self.min_x <= x <= self.max_x and self.min_y <= y <= self.max_y

    def is_miss(self, point) -> bool:
        x, y = point
        return x > self.max_x or y < self.min_y


def simulate(area: Area):
    min_vx, max_vx = 0, 1000
    min_vy, max_vy = -1000, 1000

    trajectories = []
    for vx in range(min_vx, max_vx):
        for vy in range(min_vy, max_vy):
            state = State((0, 0), (vx, vy))
            trajectory = [state]
            while not area.is_miss(state.position):
                if state.position in area:
                    trajectories.append(trajectory)
                    break
                state = state.next()
                trajectory.append(state)

    print(len(trajectories))
    max_height = max(max(state.position[1] for state in trajectory) for trajectory in trajectories)
    print(max_height)


if __name__ == '__main__':
    simulate(Area(195, 238, -93, -67))
