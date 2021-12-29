import z3


class Instruction:
    def __init__(self, code, left, right):
        self.code = code
        self.left = left
        self.right = right

    def __str__(self):
        return f'{self.code} {self.left} {self.right}'


def read_program():
    program = []
    with open('input.txt', 'r') as input_stream:
        for line in [line.rstrip() for line in input_stream]:
            elements = line.split(' ')
            code = elements[0]
            args = []
            for raw_arg in elements[1:]:
                if is_number(raw_arg):
                    args.append(int(raw_arg))
                elif raw_arg.isalpha():
                    args.append(raw_arg)
                else:
                    raise ValueError(line)
            if len(args) == 1:
                args.append(None)
            program.append(Instruction(code, args[0], args[1]))
    return program


def is_number(text: str) -> bool:
    if not text:
        return False

    if text.isnumeric():
        return True

    if text[0] == '-' and text[1:].isnumeric():
        return True

    return False


if __name__ == '__main__':
    program = read_program()
    variables = []

    for variable_number in range(1, 15):
        variable = z3.Int(f'v{variable_number}')
        variables.append(variable)

    objective = z3.IntVal(0)
    for position, variable in enumerate(variables):
        objective += 10 ** (len(variables) - position) * variable

    opt = z3.Optimize()
    for variable in variables:
        opt.add(variable >= 1)
        opt.add(variable <= 9)
    opt.minimize(objective)

    input_pos = 0
    registers = {'w': z3.IntVal(0), 'x': z3.IntVal(0), 'y': z3.IntVal(0), 'z': z3.IntVal(0)}


    def get_right(instruction: Instruction):
        if instruction.right is None:
            return None
        elif isinstance(instruction.right, int):
            return z3.IntVal(instruction.right)
        else:
            return registers[instruction.right]


    for op in program:
        right = get_right(op)
        left = registers[op.left]
        if op.code == 'inp':
            registers[op.left] = variables[input_pos]
            input_pos += 1
            assert right is None
        elif op.code == 'mul':
            if right == z3.IntVal(0):
                registers[op.left] = right
            else:
                registers[op.left] = left * right
        elif op.code == 'add':
            registers[op.left] = left + right
        elif op.code == 'div':
            right = get_right(op)
            if right == z3.IntVal(1):
                continue
            registers[op.left] = left / right
        elif op.code == 'mod':
            registers[op.left] = left % right
        elif op.code == 'eql':
            registers[op.left] = left == right
        else:
            print(op)
    opt.add(registers['z'] == 0)

    print(opt.check())
    result = opt.model()
    values = []
    for variable in variables:
        values.append(result[variable].as_string())
    print(''.join(values))
