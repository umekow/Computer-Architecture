"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.memory = [0] * 256
        self.reg = [0] * 8
        self.pc = 0 
        

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

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.memory[address] = instruction
        #     address += 1

    #arithmetic logic unit is a circuit to peform logic and arithmetic operations
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
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        
        #instructions
        PRN = 0b01000111
        HLT = 0b00000001
        LDI = 0b10000010
        r = 0

        running = True
        while running: 
            IR = self.memory[self.pc]
         

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            #print value
            if IR == PRN: 
                print(self.reg[0])
                self.pc += 1
            
            elif IR == LDI: 
                self.reg[r] = operand_b
                self.pc += 3
                r += 1

            #add
            elif IR == 0b10100000: 
                self.alu('ADD', operand_a, operand_b)
                self.pc += 3

            #subtract
            elif IR == 0b01100110: 
                self.alu('DEC', operand_a, operand_b)
                self.pc += 3


            elif IR == 0b10100011: 
                self.alu('DIV', operand_a, operand_b)
                self.pc += 3

            elif IR == 0b10100010:
                self.alu('MUL', r - 2, r - 1)
                self.pc += 3

            elif IR == HLT: 
                running = False
                self.pc = 0
            elif IR == 0b00000000:
                self.pc += 1
            else: 
                print('instruction not valid!')
            

    def ram_read(self, address): 
        return self.memory[address]

    def ram_write(self, address, value): 
        self.memory[address] = value