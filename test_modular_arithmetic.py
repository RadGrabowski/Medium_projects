from OOP.modular_arithmetic import Mod
import unittest

"""Basic tests performed on the Mod class in the modular_arithmetic file."""


class TestMod(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_create_mod(self):
        x = Mod(8, 3)
        self.assertEqual(8, x._value)
        self.assertEqual(2, x.value)
        self.assertEqual(3, x._modulus)
        self.assertEqual(3, x.modulus)

        with self.assertRaises(ValueError):
            x = Mod(8, 0)

        with self.assertRaises(ValueError):
            x = Mod(1, -1)

        with self.assertRaises(TypeError):
            x = Mod(1.5, 1)

        with self.assertRaises(TypeError):
            x = Mod(1, 1.8)

        with self.assertRaises(TypeError):
            x = Mod('d', 3)

    def test_representation(self):
        x = Mod(8, 3)
        self.assertEqual(repr(x), f'Mod({x.value}, {x.modulus})')

    def test_equality(self):
        x = Mod(8, 3)
        for mod in (Mod(8, 3), Mod(2, 3), 2, 8):
            self.assertEqual(x, mod)

        for mod in (Mod(7, 3), Mod(8, 2), 1, 9):
            self.assertNotEqual(x, mod)

    def test_hash(self):
        x = Mod(8, 3)
        self.assertEqual(hash(x), hash((x.value, x.modulus)))

    def test_int(self):
        x = Mod(8, 3)
        self.assertEqual(x.value, int(x))

    def test_neg(self):
        x = Mod(8, 3)
        self.assertEqual(-x, Mod(-8, 3))

    def test_math_operations(self):
        x = Mod(8, 3)
        y = Mod(4, 3)
        z = Mod(4, 2)
        self.assertEqual(x + y, Mod(12, 3))
        self.assertEqual(x + 5, Mod(13, 3))
        self.assertEqual(5 + x, Mod(13, 3))
        self.assertEqual(x - y, Mod(4, 3))
        self.assertEqual(x - 10, Mod(-2, 3))
        self.assertEqual(10 - x, Mod(2, 3))
        self.assertEqual(x * y, Mod(32, 3))
        self.assertEqual(x * 3, Mod(24, 3))
        self.assertEqual(3 * x, Mod(24, 3))
        self.assertEqual(x ** y, Mod(8, 3))
        self.assertEqual(x ** 5, Mod(64, 3))
        self.assertEqual(5 ** x, Mod(25, 3))
        self.assertTrue(x > y)
        self.assertTrue(x >= y)
        self.assertFalse(x < y)
        self.assertFalse(x <= y)
        with self.assertRaises(TypeError):
            x < z
        with self.assertRaises(TypeError):
            x + z
        with self.assertRaises(TypeError):
            x - z
        with self.assertRaises(TypeError):
            x * z
        with self.assertRaises(TypeError):
            x ** z


def run_tests(test_class):
    suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


run_tests(TestMod)
