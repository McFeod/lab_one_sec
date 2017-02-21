import math
from operator import add

from functools import reduce

from tours import FourthTour, ThirdTour, SecondTour, FirstTour

BUFFER_SIZE = 0xFFFFFFFF
CHUNK_SIZE = 0xFFFFFFFFFFFFFFFF


def do_nothing(*args, **kwargs):
    pass


class Md5Solver:
    init_values = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]

    def __init__(self):
        self.constants = [int(abs(math.sin(i + 1)) * 2 ** 32) & BUFFER_SIZE for i in range(64)]
        tours = FirstTour(), SecondTour(), ThirdTour(), FourthTour()
        self.functions = reduce(add, map(lambda x: [x.bit_function] * 16, tours))
        self.index_functions = reduce(add, map(lambda x: [x.index_function] * 16, tours))
        self.rotate_amounts = reduce(add, map(lambda x: x.rotate_constants() * 4, tours))
        self.data = None
        self.hash_pieces = None

    def prepare_input(self, message):
        self.data = bytearray(message)
        print('codes: ', ', '.join(str(x) for x in self.data))
        bit_size = (8 * len(self.data)) & CHUNK_SIZE
        self.data.append(0x80)
        while len(self.data) % 64 != 56:
            self.data.append(0)
        self.data += bit_size.to_bytes(8, byteorder='little')
        print('formatted: ', '{:0x}'.format(int.from_bytes(self.data, byteorder='big')))

    def round_step(self, a, b, c, d, chunk, iteration):
        def left_rotate(x, amount):
            x &= BUFFER_SIZE
            return ((x << amount) | (x >> (32 - amount))) & BUFFER_SIZE

        bit_function_result = self.functions[iteration](b, c, d)
        index = self.index_functions[iteration](iteration)
        to_rotate = a + bit_function_result + self.constants[iteration] + int.from_bytes(
            chunk[4 * index: 4 * index + 4], byteorder='little')
        new_b = (b + left_rotate(to_rotate, self.rotate_amounts[iteration])) & BUFFER_SIZE
        return d, new_b, b, c

    def solution_steps(self, message):
        self.prepare_input(message)
        self.hash_pieces = self.init_values.copy()
        for offset in range(0, len(self.data), 64):
            a, b, c, d = self.hash_pieces
            chunk = self.data[offset: offset + 64]
            for i in range(64):
                yield i, (a, b, c, d), False
                a, b, c, d = self.round_step(a, b, c, d, chunk, i)
                yield i, (a, b, c, d), True
            for idx, val in enumerate([a, b, c, d]):
                self.hash_pieces[idx] += val
                self.hash_pieces[idx] &= BUFFER_SIZE

    def md5(self, message, step_action=do_nothing):
        for step in self.solution_steps(message):
            step_action(step)
        return sum(x << (32 * i) for i, x in enumerate(self.hash_pieces))

    def md5hex(self, message, step_action=do_nothing):
        raw = self.md5(message, step_action)
        print('before_inversion:', '{:0x}'.format(raw))
        return '{:032x}'.format(int.from_bytes(raw.to_bytes(16, byteorder='little'), byteorder='big'))
