"""CPU functionality."""
#CMP
#Compare the values in two registers.


#JEQ

#JMP


#JNE

import sys

class CPU:
    """Main CPU class."""
#The SP points at the value at the top of the stack (most recently pushed), or at address F4 if the stack is empty.
#PUSH 01000101 00000rrr
#POP  01000110 00000rrr

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0 #pointer to current instruction
        self.sp = 7 # stack pointer
        self.fl = [0] * 8 #flags register

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        if len(sys.argv) < 2:
            print('No program provided')
            exit(2)

        try:
            address = 0
            fp = open(sys.argv[1], 'r')
            for line in fp:
                if line[0] == '#':
                    continue
                instruction = line.split('#')
                instruction = instruction[0].strip()
                if instruction == "":
                    continue
                self.ram[address] = int(instruction, 2)
                address += 1

        except FileNotFoundError:
            print(f"File not found: {sys.argv[1]}")
            exit(2) 

        # For now, we've just hardcoded a program:

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
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.fl,
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
        cpu_running = True
        while cpu_running:
            #HLT
            if self.ram[self.pc] == 0b00000001:
                exit(1)
            #LDI
            elif self.ram[self.pc] == 0b10000010:
                register = self.ram_read(self.pc+1)
                value = self.ram_read(self.pc+2)
                self.reg[register] = value
                self.pc += 3
            #PRN
            elif self.ram[self.pc] == 0b01000111:
                print(self.reg[self.ram_read(self.pc+1)])
                self.pc += 2
            #MUL
            elif self.ram[self.pc] == 0b10100010:
                operand_1 = self.reg[self.ram_read(self.pc+1)]
                operand_2 = self.reg[self.ram_read(self.pc+2)]
                self.reg[self.ram_read(self.pc+1)] = operand_1 * operand_2
                self.pc += 3
            #PUSH
            elif self.ram[self.pc] == 0b01000101:
                reg = self.ram[self.pc + 1]
                val = self.reg[reg]
                self.reg[self.sp] -= 1
                self.ram[self.reg[self.sp]] = val
                self.pc += 2
            #POP
            elif self.ram[self.pc] == 0b01000110:
                reg = self.ram[self.pc + 1]
                val = self.ram[self.reg[self.sp]]
                self.reg[reg] = val
                self.reg[self.sp] += 1
                self.pc += 2
            #JNE
            elif self.ram[self.pc] == 0b01010110:
                # If E flag is clear (false, 0), jump to the address stored in the given register.
                if self.fl[7]== 0:
                    self.pc = self.reg[self.ram_read(self.pc+1)]
                else:
                    self.pc += 2
            #CMP
            elif self.ram[self.pc] == 0b10100111:
                reg_a = self.reg[self.ram_read(self.pc+1)]
                reg_b = self.reg[self.ram_read(self.pc+2)]
                #If they are equal, set the Equal E flag to 1, otherwise set it to 0.
                if reg_a == reg_b:
                    self.fl[7] = 1
                #If registerA is less than registerB, set the Less-than L flag to 1, otherwise set it to 0.
                elif reg_a < reg_b:
                    self.fl[5] = 1
                #If registerA is greater than registerB, set the Greater-than G flag to 1, otherwise set it to 0.
                elif reg_a > reg_b:
                    self.fl[6] = 1
                self.pc += 3
            #JEQ    
            elif self.ram[self.pc] == 0b01010101:
            #If equal flag is set (true), jump to the address stored in the given register.
                if self.fl[7] == 1:
                    self.pc = self.reg[self.ram_read(self.pc+1)]
                else:
                    self.pc += 2
            # JMP
            elif self.ram[self.pc] == 0b01010100:
                #Jump to the address stored in the given register.
                register = self.ram_read(self.pc+1)
                #Set the PC to the address stored in the given register.
                self.pc = register
                self.pc += 2