from __future__ import print_function
from collections import defaultdict
import sys


if sys.version[0] == '3':
    def raw_input(x):
        return str(input(x))


def _printf(x):
    print(x, end='')


class Interpreter(object):

    def __init__(self):
        self.data_pointer = 0
        self.memory = defaultdict(lambda *_: 0)
        self.input_func = lambda : int(raw_input('\nEnter input : '))
        self.output_func = _printf

    def set_input_hook(self, func):
        self.input_func = func

    def set_output_hook(self, func):
        self.output_func = func

    def reset(self):
        self.data_pointer = 0
        keys = list(self.memory.keys())
        for k in keys:
           del self.memory[k]

    def execute(self, code):
        memory = self.memory
        stack = []
        inp = self.input_func
        out = self.output_func
        instruction_pointer = 0
        data_pointer = self.data_pointer
        stack_push = stack.append
        stack_pop = stack.pop
        skip = 0
        final_instruction = len(code) - 1
        while(True):
            x = code[instruction_pointer]
            if skip:
                if x == '[':
                    skip += 1
                elif skip == ']':
                    skip -= 1
            elif x == '+':
                memory[data_pointer] += 1
            elif x == '-':
                memory[data_pointer] -= 1
            elif x == '>':
                data_pointer += 1
            elif x == '<':
                if not data_pointer:
                    raise Exception("Invalid index to memory : -1")
                data_pointer -= 1
            elif x == '[':
                if memory[data_pointer]:
                    stack_push(instruction_pointer + 1)
                else:
                    skip = 1
            elif x == ']':
                if memory[data_pointer]:
                    instruction_pointer = stack[-1]
                    continue
                else:
                    stack_pop()
            elif x == ',':
                memory[data_pointer] = inp()
            elif x == '.':
                out(chr(memory[data_pointer]))
            if instruction_pointer == final_instruction:
                break
            else:
                instruction_pointer += 1
        self.data_pointer = data_pointer

    def evaluate(self, code, input=None):
        memory = defaultdict(lambda *_: 0)
        stack = []
        instruction_pointer = 0
        data_pointer = 0
        stack_push = stack.append
        stack_pop = stack.pop
        skip = 0
        final_instruction = len(code) - 1
        output = ''
        if input is None:
            def inp():
                raise Exception("No input provided")
        else:
            input_idx = 0
            def inp():
                i = input[input_idx]
                input_idx += 1
                return i
        while(True):
            x = code[instruction_pointer]
            if skip:
                if x == '[':
                    skip += 1
                elif skip == ']':
                    skip -= 1
            elif x == '+':
                memory[data_pointer] += 1
            elif x == '-':
                memory[data_pointer] -= 1
            elif x == '>':
                data_pointer += 1
            elif x == '<':
                if not data_pointer:
                    raise Exception("Invalid index to memory : -1")
                data_pointer -= 1
            elif x == '[':
                if memory[data_pointer]:
                    stack_push(instruction_pointer + 1)
                else:
                    skip = 1
            elif x == ']':
                if memory[data_pointer]:
                    instruction_pointer = stack[-1]
                    continue
                else:
                    stack_pop()
            elif x == ',':
                memory[data_pointer] = inp()
            elif x == '.':
                output += chr(memory[data_pointer])
            if instruction_pointer == final_instruction:
                break
            else:
                instruction_pointer += 1
        return output

    def cli(self):
        def help():
            print("=======Brainfuck CLI=======")
            print("Type \"mem\" to see memory contents.")
            print("Type \"dp\" to see data pointer value.")
            print("Type \"reset\" to reset interpreter state.")
            print("Type \"exit\" to exit cli.")
        help()
        while(True):
            try:  
                input = raw_input('\nEnter input : ').lower().strip()
                if input == 'exit':
                    break
                elif input == 'mem':
                    dp = self.data_pointer
                    memory = self.memory
                    mem_size = max(list(memory.keys()) + [dp]) + 1
                    elems = [str(memory[i]) for i in range(mem_size)]
                    elems[dp] = '>' + elems[dp]
                    print(' '.join(elems))
                elif input == 'dp':
                    print(self.data_pointer)
                elif input == "reset":
                    self.reset()
                elif input == "help":
                    help()
                else:
                    self.execute(input)
            except Exception as e:
                print(e)

