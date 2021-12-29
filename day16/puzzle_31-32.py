from typing import Tuple, List

CODE_MAP = {'0': '0000',
            '1': '0001',
            '2': '0010',
            '3': '0011',
            '4': '0100',
            '5': '0101',
            '6': '0110',
            '7': '0111',
            '8': '1000',
            '9': '1001',
            'A': '1010',
            'B': '1011',
            'C': '1100',
            'D': '1101',
            'E': '1110',
            'F': '1111'}


def hex_to_bin(hex_segment: str) -> str:
    output_value = []
    for code in hex_segment:
        output_value.append(CODE_MAP[code])
    return ''.join(output_value)


#   111000000000000110111101000101001010010001001000000000
# 0011 1000 0000 0000 0110 1111 0100 0101 0010 1001 0001 0010 0000 0000
# VVVTTTLNNNNNNNNNNNNNNN

class Reader:

    def __init__(self, bin_segment: str):
        self.bin_segment = bin_segment
        self.offset = 0

    def read(self, num_bytes: int) -> str:
        next_offset = self.offset + num_bytes
        value = self.bin_segment[self.offset: next_offset]
        self.offset = next_offset
        return value

    def has_next(self):
        return self.offset < len(self.bin_segment)

    def read_int(self, num_bytes: int) -> int:
        bytes = self.read(num_bytes)
        return int(bytes, 2)

    @classmethod
    def from_hex_segment(cls, hex_segment: str):
        bin_segment = hex_to_bin(hex_segment)
        return cls(bin_segment)


def get_header(reader: Reader) -> Tuple[int, int]:
    version = reader.read_int(3)
    packet_type = reader.read_int(3)
    return version, packet_type


class Packet(object):
    def __init__(self, version: int, packet_type: int):
        self.version = version
        self.packet_type = packet_type

    def calculate(self) -> int:
        return 0

    def version_sum(self):
        return self.version


class NumberPacket(Packet):

    def __init__(self, version: int, packet_type: int, value: int):
        super(NumberPacket, self).__init__(version, packet_type)
        self.value = value

    def calculate(self):
        return self.value

    def __str__(self):
        return str(self.value)


class OperatorPacket(Packet):

    def __init__(self, version: int, packet_type: int, sub_packets: List[Packet]):
        super(OperatorPacket, self).__init__(version, packet_type)
        self.sub_packets = sub_packets

    def calculate(self) -> int:
        values = [sub_packet.calculate() for sub_packet in self.sub_packets]
        if self.packet_type == 0:
            return sum(values)
        if self.packet_type == 1:
            result = values[0]
            for value in values[1:]:
                result *= value
            return result
        if self.packet_type == 2:
            return min(values)
        if self.packet_type == 3:
            return max(values)
        if self.packet_type == 5:
            return int(values[0] > values[1])
        if self.packet_type == 6:
            return int(values[0] < values[1])
        if self.packet_type == 7:
            return int(values[0] == values[1])

    def version_sum(self):
        total_version_sum = self.version
        for packet in self.sub_packets:
            total_version_sum += packet.version_sum()
        return total_version_sum


def parse_number(reader: Reader) -> int:
    groups = []
    while True:
        is_last = reader.read(1) == '0'
        groups.append(reader.read(4))
        if is_last:
            break
    return int(''.join(groups), 2)


def parse(reader: Reader) -> Packet:
    version, packet_type = get_header(reader)
    if packet_type == 4:
        number = parse_number(reader)
        return NumberPacket(version, packet_type, number)
    else:
        length_type_id = reader.read(1)
        if length_type_id == '1':
            num_sub_packets = reader.read_int(11)
            sub_packets = []
            for _ in range(num_sub_packets):
                packet = parse(reader)
                sub_packets.append(packet)
            return OperatorPacket(version, packet_type, sub_packets)
        elif length_type_id == '0':
            total_length = reader.read_int(15)
            bytes = reader.read(total_length)
            inner_reader = Reader(bytes)
            sub_packets = []
            while inner_reader.has_next():
                packet = parse(inner_reader)
                sub_packets.append(packet)
            return OperatorPacket(version, packet_type, sub_packets)
        else:
            raise ValueError()


if __name__ == '__main__':
    reader = Reader.from_hex_segment('E20D72805F354AE298E2FCC5339218F90FE5F3A388BA60095005C3352CF7FBF27CD4B3DFEFC95354723006C401C8FD1A23280021D1763CC791006E25C198A6C01254BAECDED7A5A99CCD30C01499CFB948F857002BB9FCD68B3296AF23DD6BE4C600A4D3ED006AA200C4128E10FC0010C8A90462442A5006A7EB2429F8C502675D13700BE37CF623EB3449CAE732249279EFDED801E898A47BE8D23FBAC0805527F99849C57A5270C064C3ECF577F4940016A269007D3299D34E004DF298EC71ACE8DA7B77371003A76531F20020E5C4CC01192B3FE80293B7CD23ED55AA76F9A47DAAB6900503367D240522313ACB26B8801B64CDB1FB683A6E50E0049BE4F6588804459984E98F28D80253798DFDAF4FE712D679816401594EAA580232B19F20D92E7F3740D1003880C1B002DA1400B6028BD400F0023A9C00F50035C00C5002CC0096015B0C00B30025400D000C398025E2006BD800FC9197767C4026D78022000874298850C4401884F0E21EC9D256592007A2C013967C967B8C32BCBD558C013E005F27F53EB1CE25447700967EBB2D95BFAE8135A229AE4FFBB7F6BC6009D006A2200FC3387D128001088E91121F4DED58C025952E92549C3792730013ACC0198D709E349002171060DC613006E14C7789E4006C4139B7194609DE63FEEB78004DF299AD086777ECF2F311200FB7802919FACB38BAFCFD659C5D6E5766C40244E8024200EC618E11780010B83B09E1BCFC488C017E0036A184D0A4BB5CDD0127351F56F12530046C01784B3FF9C6DFB964EE793F5A703360055A4F71F12C70000EC67E74ED65DE44AA7338FC275649D7D40041E4DDA794C80265D00525D2E5D3E6F3F26300426B89D40094CCB448C8F0C017C00CC0401E82D1023E0803719E2342D9FB4E5A01300665C6A5502457C8037A93C63F6B4C8B40129DF7AC353EF2401CC6003932919B1CEE3F1089AB763D4B986E1008A7354936413916B9B080')
    packet = parse(reader)
    print(packet.calculate())
