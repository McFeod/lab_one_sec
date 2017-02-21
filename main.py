import hashlib

from md5_solver import Md5Solver


def pretty_print(data):
    iteration, chunks, finished = data

    if (iteration + 1) % 16 < 3:

        print('{} tour {}, iteration {}: {}'.format(
            'after' if finished else 'before',
            iteration // 16 + 1,
            iteration % 16 + 1,
            ', '.join(map(lambda x: '{:08x}'.format(x), chunks))
        ))


def use_1251(func):
    def wrapper(data, *args, **kwargs):
        return func(data.encode('cp1251'), *args, **kwargs)
    return wrapper


@use_1251
def correct_md5(data):
    return hashlib.md5(data).hexdigest()


@use_1251
def custom_md5(data, solver=None):
    if solver is None:
        solver = Md5Solver()
    return solver.md5hex(data, pretty_print)


if __name__ == '__main__':
    demo = ["Фед", "a", "abc", "фыва", "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
            "12345678901234567890123456789012345678901234567890123456789012345678901234567890"]
    md5_solver = Md5Solver()
    for message in demo:
        print('string: ', message)
        print('result: ', custom_md5(message, md5_solver))
        print('expected result: ', correct_md5(message))
        print('-'*80)
