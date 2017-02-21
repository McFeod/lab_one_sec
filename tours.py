from abc import abstractmethod


class Tour:
    @abstractmethod
    def bit_function(self, x, y, z):
        pass

    @abstractmethod
    def index_function(self, i):
        pass

    @abstractmethod
    def rotate_constants(self):
        pass


class FirstTour(Tour):
    def rotate_constants(self):
        return [7, 12, 17, 22]

    def bit_function(self, x, y, z):
        return (x & y) | (~x & z)

    def index_function(self, i):
        return i


class SecondTour(Tour):
    def rotate_constants(self):
        return [5, 9, 14, 20]

    def bit_function(self, x, y, z):
        return (z & x) | (~z & y)

    def index_function(self, i):
        return (5 * i + 1) % 16


class ThirdTour(Tour):
    def rotate_constants(self):
        return [4, 11, 16, 23]

    def bit_function(self, x, y, z):
        return x ^ y ^ z

    def index_function(self, i):
        return (3 * i + 5) % 16


class FourthTour(Tour):
    def rotate_constants(self):
        return [6, 10, 15, 21]

    def bit_function(self, x, y, z):
        return y ^ (x | ~z)

    def index_function(self, i):
        return (7 * i) % 16
