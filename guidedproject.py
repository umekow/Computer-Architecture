PRINT_UMEKO = 1
HALT = 2
SAVE_REG = 3  # Store a value in register (LDI)
PRINT_REG = 4  # PRN in LS8

memory = [
    PRINT_UMEKO,
    SAVE_REG,  # SAVE r0, 37 -- opcode
    0,  # register   operand ('argument)
    37,  # 37    operand
    PRINT_UMEKO,
    PRINT_REG,
    0,

    HALT
]

register = [0] * 8

pc = 0  # counter

running = True


while running:
    inst = memory[pc]

    if inst == 1:
        print('Umeko Walker')
        pc += 1
    elif inst == SAVE_REG:
        reg_num = memory[pc + 1]
        value = memory[pc + 2]
        register[reg_num] = value
        pc += 3
    elif inst == 2:
        running = False

    elif inst == PRINT_REG:
        reg_num = memory[pc + 1]
        value = register[reg_num]
        print(value)
        pc += 2
    else:
        print('Unknown instruction')
        running = False
