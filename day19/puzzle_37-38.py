import re
from typing import Tuple, Optional

SCANNER_PATTERN = re.compile(r'---\s+scanner\s+(?P<scanner>\d+)\s+---')
BEACON_PATTERN = re.compile(r'(?P<x>-?\d+),\s*(?P<y>-?\d+),\s*(?P<z>-?\d+)')


class Point3D:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        elif item == 2:
            return self.z
        raise ValueError()

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        elif key == 2:
            self.z = value
        else:
            raise ValueError()

    def __add__(self, other):
        if isinstance(other, Point3D):
            return Point3D(self.x + other.x, self.y + other.y, self.z + other.z)
        raise ValueError()

    def __sub__(self, other):
        if isinstance(other, Point3D):
            return Point3D(self.x - other.x, self.y - other.y, self.z - other.z)
        raise ValueError()

    def __mul__(self, other):
        if isinstance(other, Point3D):
            return self.x * other.x + self.y * other.y + self.z * other.z
        if isinstance(other, Orientation3D):
            return Point3D(other.x * self, other.y * self, other.z * self)
        raise ValueError()

    def __eq__(self, other):
        if isinstance(other, Point3D):
            return self.x == other.x and self.y == other.y and self.z == other.z
        return False

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __str__(self):
        return (self.x, self.y, self.z).__str__()

    def __lt__(self, other):
        if isinstance(other, Point3D):
            if self.x < other.x:
                return True
            elif self.x == other.x and self.y < other.y:
                return True
            elif self.x == other.x and self.y == other.y and self.z < other.z:
                return True
            return False
        raise ValueError()


class Orientation3D:

    def __init__(self, x: Point3D, y: Point3D, z: Point3D):
        self.x = x
        self.y = y
        self.z = z

    def __mul__(self, other):
        if isinstance(other, Orientation3D):
            return Orientation3D(Point3D(self.x * other.x, 0, 0),
                                 Point3D(0, self.y * other.y, 0),
                                 Point3D(0, 0, self.z * other.z))
        else:
            raise ValueError()


IDENTITY_ORIENTATION = Orientation3D(Point3D(1, 0, 0), Point3D(0, 1, 0), Point3D(0, 0, 1))
IDENTITY_OFFSET = Point3D(0, 0, 0)


class BeaconSet:

    def __init__(self, beacons):
        self.beacons = list(beacons)
        self.distances = self.__compute_distances()

    def translate(self, orientation):
        beacons = [beacon * orientation for beacon in self.beacons]
        return BeaconSet(beacons)

    def get_match(self, beacon, other: 'BeaconSet'):
        matched_beacons = []
        for other_beacon in other.beacons:
            same_distance_beacons = []
            for distance in self.distances[beacon]:
                same_distance_beacons.extend(other.distances[other_beacon].get(distance, []))
            if len(same_distance_beacons) >= 11:
                matched_beacons.append(other_beacon)
        if not matched_beacons:
            return None
        assert len(matched_beacons) == 1
        return matched_beacons[0]

    def __get_diff(self):
        diff = []
        prev = self.beacons[0]
        for beacon in self.beacons[1:]:
            diff.append((beacon.x - prev.x, beacon.y - prev.y, beacon.z - prev.z))
            prev = beacon
        return diff

    def get_rotation(self, other: 'BeaconSet'):
        diff = self.__get_diff()
        other_diff = other.__get_diff()

        rotations = []
        for pos in range(3):
            point = Point3D(0, 0, 0)
            other_pos = [i for i in range(0, 3) \
                         if all(abs(diff[row][pos]) == abs(other_diff[row][i]) for row in range(len(diff)))]
            assert len(other_pos) == 1
            other_pos = other_pos[0]
            point[other_pos] = 1 if all(
                diff[row][pos] == other_diff[row][other_pos] for row in range(len(diff))) else -1
            rotations.append(point)

        assert sum([abs(rotation.x) for rotation in rotations]) == 1
        assert [abs(rotation.x) + abs(rotation.y) + abs(rotation.z) for rotation in rotations] == [1, 1, 1]

        return Orientation3D(*rotations)

    def __compute_distances(self):
        distance_matrix = {beacon: dict() for beacon in self.beacons}
        num_beacons = len(self.beacons)

        def add_distance(from_node, to_node, local_distance):
            from_distance_matrix = distance_matrix[from_node]
            if local_distance not in from_distance_matrix:
                from_distance_matrix[local_distance] = [to_node]
            else:
                from_distance_matrix[local_distance].append(to_node)

        for left_index in range(num_beacons):
            left = self.beacons[left_index]
            for right_index in range(left_index + 1, num_beacons):
                right = self.beacons[right_index]
                distance = self.distance(left, right)
                add_distance(left, right, distance)
                add_distance(right, left, distance)
        return distance_matrix

    @staticmethod
    def distance(left: Point3D, right: Point3D):
        return abs(left.x - right.x) + abs(left.y - right.y) + abs(left.z - right.z)


class Scanner:

    def __init__(self, number, beacons, offset=None):
        self.number = number
        self.beacons = beacons
        self.offset = offset

    def apply_offset(self, offset):
        beacons = [beacon + offset for beacon in self.beacons]
        return Scanner(self.number, beacons, offset)

    def apply_rotation(self, orientation):
        beacons = [beacon * orientation for beacon in self.beacons]
        return Scanner(self.number, beacons, self.offset)


class OverlapResult:

    def __init__(self, offset, rotation):
        self.offset = offset
        self.rotation = rotation


def compute_overlap(left_scanner: Scanner, right_scanner: Scanner) -> Optional[OverlapResult]:
    left_beacons = BeaconSet(left_scanner.beacons)
    right_beacons = BeaconSet(right_scanner.beacons)

    while True:
        left_next_round = set()
        right_next_round = set()
        for left_beacon in left_beacons.beacons:
            right_beacon = left_beacons.get_match(left_beacon, right_beacons)
            if right_beacon:
                left_next_round.add(left_beacon)
                right_next_round.add(right_beacon)
        if all(beacon in left_next_round for beacon in left_beacons.beacons) \
                and all(beacon in right_next_round for beacon in right_beacons.beacons):
            break
        left_beacons = BeaconSet(left_next_round)
        right_beacons = BeaconSet(right_next_round)

    if len(left_beacons.beacons) < 12 or len(right_beacons.beacons) < 12:
        return None

    matched_left_beacons = []
    matched_right_beacons = []
    for left_beacon in left_beacons.beacons:
        matched_left_beacons.append(left_beacon)
        matched_right_beacons.append(left_beacons.get_match(left_beacon, right_beacons))
    left_beacons = BeaconSet(matched_left_beacons)
    right_beacons = BeaconSet(matched_right_beacons)
    rotation = left_beacons.get_rotation(right_beacons)
    left_beacon = matched_left_beacons[0]
    right_beacon = matched_right_beacons[0]
    right_translated_beacon = right_beacon * rotation
    offset = left_beacon - right_translated_beacon
    return OverlapResult(offset, rotation)


def load_test_input():
    scanners = []
    with open('input.txt', 'r') as input_stream:
        scanner_number = None
        beacons = list()
        for line in input_stream:
            scanner_match = SCANNER_PATTERN.match(line)
            if scanner_match:
                if scanner_number is not None:
                    scanners.append(Scanner(scanner_number, beacons))
                scanner_number = int(scanner_match.group('scanner'))
                beacons = list()

            beacon_match = BEACON_PATTERN.match(line)
            if beacon_match:
                beacon = Point3D(*[int(beacon_match.group(coordinate)) for coordinate in ['x', 'y', 'z']])
                beacons.append(beacon)

        if scanner_number is not None:
            scanners.append(Scanner(scanner_number, beacons))
    return scanners


if __name__ == '__main__':
    scanners = load_test_input()
    scanners[0].offset = Point3D(0, 0, 0)
    num_scanners = len(scanners)
    scanner_by_id = {scanner.number: scanner for scanner in scanners}

    resolved_scanner_ids = set()
    resolved_scanner_ids.add(0)

    while len(resolved_scanner_ids) < num_scanners:
        remaining_scanner_ids = [scanner_id for scanner_id in scanner_by_id if scanner_id not in resolved_scanner_ids]
        for resolved_scanner_id in list(resolved_scanner_ids):
            resolved_scanner = scanner_by_id[resolved_scanner_id]
            for other_scanner_id in list(remaining_scanner_ids):
                other_scanner = scanner_by_id[other_scanner_id]
                result = compute_overlap(resolved_scanner, other_scanner)
                if result:
                    rotated_scanner = other_scanner.apply_rotation(result.rotation)
                    scanner = rotated_scanner.apply_offset(result.offset)
                    scanner_by_id[scanner.number] = scanner
                    resolved_scanner_ids.add(scanner.number)
                    remaining_scanner_ids.remove(scanner.number)

    resolved_scanners = list(scanner_by_id.values())
    distances = []
    for left in range(len(resolved_scanners)):
        left_scanner = resolved_scanners[left]
        for right in range(left + 1, len(resolved_scanners)):
            right_scanner = resolved_scanners[right]
            distances.append(BeaconSet.distance(left_scanner.offset, right_scanner.offset))
    print(max(distances))
