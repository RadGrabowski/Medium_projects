from functools import total_ordering


@total_ordering  # helps with defining comparisons, only one is then required, i.e. __lt__
class Mod:
    """
    This class implements some concepts of modular arithmetic.
    We instantiate the class with two integer values: the value and the modulus.
    The modulus must be a positive number.
    We can also perform some basic mathematical operations on two instances or an instance with an integer.
    Comparison is also available.
    """
    def __init__(self, value: int, modulus: int):
        if isinstance(value, int) and isinstance(modulus, int):
            self._value = value
            if modulus > 0:
                self._modulus = modulus
            else:
                raise ValueError('Modulus must be a positive integer.')
        else:
            raise TypeError('Unsupported type.')

    @property
    def value(self):
        return self._value % self.modulus

    @property
    def modulus(self):
        return self._modulus

    def __repr__(self):
        return f'Mod({self.value}, {self.modulus})'

    def __eq__(self, other):
        try:
            other_value = self._get_value(other)
            return self.value == other_value
        except TypeError:
            return False

    def __hash__(self):
        return hash((self.value, self.modulus))

    def __int__(self):
        return self.value

    def __neg__(self):
        return self.__class__(-self.value, self.modulus)

    def __add__(self, other):
        other_value = self._get_value(other)
        return self.__class__(self._value + other_value, self.modulus)

    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        other_value = self._get_value(other)
        self._value += other_value
        return self

    def __sub__(self, other):
        other_value = self._get_value(other)
        return self.__class__(self._value - other_value, self.modulus)

    def __rsub__(self, other):
        other_value = self._get_value(other)
        return self.__class__(other_value - self._value, self.modulus)

    def __isub__(self, other):
        other_value = self._get_value(other)
        self._value -= other_value
        return self

    def __mul__(self, other):
        other_value = self._get_value(other)
        return self.__class__(self._value * other_value, self.modulus)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __imul__(self, other):
        other_value = self._get_value(other)
        self._value *= other_value
        return self

    def __pow__(self, other, modulo=None):
        other_value = self._get_value(other)
        return self.__class__(self._value ** (other_value % self.modulus), self.modulus)  # power % self.modulus to
        # prevent calculations of huge numbers

    def __rpow__(self, other):
        return self.__pow__(other)

    def __ipow__(self, other):
        other_value = self._get_value(other)
        self._value **= other_value
        return self

    def __lt__(self, other):
        other_value = self._get_value(other)
        return self.value < other_value % self.modulus

    def _get_value(self, other):
        if isinstance(other, int):
            return other % self.modulus
        elif isinstance(other, self.__class__) and self.modulus == other.modulus:
            return other.value
        else:
            raise TypeError('Incompatible types')


if __name__ == '__main__':
    x = Mod(8, 3)
    print(x.value, x.modulus)
    print(x == Mod(14, 4))
    print(hash(x))
    print(x)
    print(int(x))
    print(x.__dict__)
    print(x + 5 == x + Mod(5, 3))
    print(5 + x, x + 5)
    x += 7
    print(x)
    print(x * 5 == x * Mod(5, 3))
    print(5 * x, x * 5)
    x *= 7
    print(x)
    print(x >= 5)
    print(10-Mod(2, 3))
