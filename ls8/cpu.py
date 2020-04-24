"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        self.memory = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7
        self.reg[self.sp] = 0xF4  # stack pointer
        self.fl = 0b00000000

    def load(self, filename):
        """Load a program into memory."""
        address = 0

        # For now, we've just hardcoded a program:

        with open(filename) as f:
            for line in f:
                line = line.split('#')
                line = line[0].strip()

                if line == '':
                    continue

                self.memory[address] = int(line, 2)

                address += 1
        f.close()

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "DEC":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == 'MUL':

            self.reg[reg_a] *= self.reg[reg_b]
        elif op == 'DIV':
            self.reg[reg_a] / self.reg[reg_b]
        elif op == 'CMP':
            if reg_a == reg_b:
                self.fl = 0b00000001
            elif reg_a > reg_b:
                self.fl = 0b00000010
            else:
                self.fl = 0b00000100
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        # instructions
        # arithmetic
        ADD = 0b10100000
        SUB = 0b01100110
        DIV = 0b10100011
        MUL = 0b10100010

        PRN = 0b01000111
        HLT = 0b00000001
        LDI = 0b10000010
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001

        CMP = 0b10100111
        JMP = 0b01010100
        JEQ = 0b01010101
        JNE = 0b01010110

        AND = 0b10101000

        running = True
        while running:
            IR = self.memory[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # print value
            if IR == PRN:
                address = operand_a
                print(self.reg[address])
                self.pc += 2
            elif IR == LDI:
                # the register to store value
                address = operand_a
                # the value
                value = operand_b
                self.reg[address] = value
                # move to next instruction
                self.pc += 3
            # add
            elif IR == ADD:
                self.alu('ADD', operand_a, operand_b)
                self.pc += 3
            # subtract
            elif IR == SUB:
                self.alu('DEC', operand_a, operand_b)
                self.pc += 3
            # division
            elif IR == DIV:
                self.alu('DIV', operand_a, operand_b)
                self.pc += 3
            # multiplication
            elif IR == MUL:
                self.alu('MUL', operand_a, operand_b)
                self.pc += 3
            # stop
            elif IR == HLT:
                running = False
                self.pc = 0
            # push
            elif IR == PUSH:
                # decrement sp
                self.reg[self.sp] -= 1
                # get next address for register
                reg_num = self.memory[self.pc + 1]
                value = self.reg[reg_num]
                # address in memory to store value in
                address = self.reg[self.sp]
                self.memory[address] = value
                self.pc += 2
            # pop
            elif IR == POP:
                # Copy the value from the address pointed to by `SP`
                reg_num = self.memory[self.pc + 1]
                address = self.reg[self.sp]
                value = self.memory[address]
                self.reg[reg_num] = value
                # Increment `SP`
                self.reg[self.sp] += 1
                self.pc += 2
            elif IR == CALL:
                # getting return address
                return_address = self.pc + 2
                # push the return address to the stack
                self.reg[self.sp] -= 1
                value = self.reg[self.sp]
                self.memory[value] = return_address
                reg_num = self.memory[self.pc + 1]
                destination = self.reg[reg_num]
                self.pc = destination
            elif IR == RET:
                # pop return address
                value = self.reg[self.sp]
                return_address = self.memory[value]
                self.reg[self.sp] += 1
                # change the pc to return address or what it was doing before
                self.pc = return_address
            elif IR == CMP:
                # compares the values of two registers
                # get the value of two registers
                reg_value1 = self.reg[operand_a]
                reg_value2 = self.reg[operand_b]
                self.alu('CMP', reg_value1, reg_value2)
                self.pc += 3
            elif IR == JMP:
                # Jump to the address stored in the given register
                # Set the `PC` to the address stored in the given register
                address = self.reg[operand_a]
                self.pc = address

            elif IR == JEQ:
                # If `equal` flag is set (true), jump to the address stored in the given register
                if self.fl == 0b00000001:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2
            elif IR == JNE:
                # If `E` flag is clear (false, 0), jump to the address stored in the given register.
                if self.fl != 0b00000001:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2
            elif IR == AND:
                pass
            else:
                print('instruction not valid!')

    def ram_read(self, address):
        return self.memory[address]

    def ram_write(self, address, value):
        self.memory[address] = value
