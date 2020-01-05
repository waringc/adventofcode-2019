class intcode_computer(object):
    def __init__(self, opcodes):
        self.instruct_ptr = 0
        self.relative_base = 0
        self.memory = [int(i) for i in opcodes.split(',')]
        #print("Loaded computer of length: " + str(len(self.memory)))
        #instruction lengths
        self.instruct_length = [4,4,2,2,3,3,4,4,2]

    def getInstruct(self):
        opcode = str(self.memory[self.instruct_ptr]).zfill(5)
        instruction = int(opcode[-2:])
        return instruction

    def setMemory(self, location, value):
        self.memory[location] = value
        return

    def getPtr(self):
        return self.instruct_ptr


    def __check_mem(self, location):
        #print("Checking:" + str(location))
        #print(len(self.memory))
        if location >= len(self.memory):
            #print("Padding memory to length: " + str(location))
            self.memory.extend([0 for _ in range(abs(location - len(self.memory)) + 1000)])
        return

    def run(self, signal = []):

        while self.memory[self.instruct_ptr] != 99:

            #pad instruction to standard length of 5 with leading zeros
            opcode = str(self.memory[self.instruct_ptr]).zfill(5)
            instruction = int(opcode[-2:])

            #store modes and values
            modes = [int(opcode[2]), int(opcode[1]), int(opcode[0])]
            val = [0,0,0]
            mem_loc = [0,0,0]
            #print("opcode:" + str(opcode))
            
            #get position or immediate value
            for i in range(self.instruct_length[instruction - 1] - 1):
                if modes[i] == 0:

                    #check if enough memory
                    self.__check_mem(self.memory[self.instruct_ptr + 1 + i])

                    val[i] =  self.memory[self.memory[self.instruct_ptr + 1 + i]]
                    mem_loc[i] = self.memory[self.instruct_ptr + 1 + i]

                elif modes[i] == 2:
                    #check if enough memory
                    self.__check_mem(self.memory[self.instruct_ptr + 1 + i] + self.relative_base)

                    val[i] = self.memory[self.memory[self.instruct_ptr + 1 + i] + self.relative_base]
                    mem_loc[i] = self.memory[self.instruct_ptr + 1 + i] + self.relative_base

                else:
                    #check if enough memory
                    self.__check_mem(self.instruct_ptr + 1 + i)

                    val[i] = self.memory[self.instruct_ptr + 1 + i]
                    mem_loc[i] = self.instruct_ptr + 1 + i

            #add
            if instruction == 1:
                self.memory[mem_loc[2]] = val[0] + val[1]
                self.instruct_ptr += self.instruct_length[instruction - 1]

            #multiply
            elif instruction == 2:
                self.memory[mem_loc[2]] = val[0] * val[1]
                self.instruct_ptr += self.instruct_length[instruction - 1]

            #get input
            elif instruction == 3:

                if not signal:
                    return -1

                #if we have input
                user_input = int(signal.pop(0))
                self.memory[mem_loc[0]] = user_input

                self.instruct_ptr += self.instruct_length[instruction - 1]

            #output location
            elif instruction == 4:
                self.instruct_ptr += self.instruct_length[instruction - 1]
                return str(val[0])

            #jump true
            elif instruction == 5:

                if val[0] != 0:
                    self.instruct_ptr = val[1]
                else:
                    self.instruct_ptr += self.instruct_length[instruction - 1]

            #jump false
            elif instruction == 6:

                if val[0] == 0:
                    self.instruct_ptr = val[1]
                else:
                    self.instruct_ptr += self.instruct_length[instruction - 1]

            #less than
            elif instruction == 7:

                if val[0] < val[1]:
                    self.memory[mem_loc[2]] = 1
                else:
                    self.memory[mem_loc[2]] = 0

                self.instruct_ptr += self.instruct_length[instruction - 1]

            #equals
            elif instruction == 8:

                if val[0] == val[1]:
                    self.memory[mem_loc[2]] = 1
                else:
                    self.memory[mem_loc[2]] = 0

                self.instruct_ptr += self.instruct_length[instruction - 1]

            #program exit
            elif instruction == 9:
                self.relative_base += val[0]
                self.instruct_ptr += self.instruct_length[instruction - 1]

            #program exit
            elif instruction == 99:
                 return

        return
