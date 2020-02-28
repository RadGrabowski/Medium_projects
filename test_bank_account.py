from OOP.bank_account import Timezone, Account
from datetime import datetime, timedelta
import unittest

"""Basic tests performed on the classes in bank_account file."""

class TestAccount(unittest.TestCase):
    def setUp(self) -> None:
        self.account_number = 'A100'
        self.first_name = 'FIRST'
        self.last_name = 'LAST'
        self.tz = Timezone('TZ', 1, 30)
        self.balance = 100.0

    def test_create_timezone(self):
        tz = Timezone('ABC', -1, -30)
        self.assertEqual('ABC', tz.name)
        self.assertEqual(timedelta(hours=-1, minutes=-30), tz.offset)

    def test_timezone_equal(self):
        tz1 = Timezone('ABC', -1, -30)
        tz2 = Timezone('ABC', -1, -30)
        self.assertEqual(tz1, tz2)

    def test_timezones_not_equal(self):
        tz1 = Timezone('ABC', -1, -30)
        test_timezones = (Timezone('DEF', -1, -30), Timezone('ABC', -1, 0), Timezone('ABC', 1, -30))
        for test_tz in test_timezones:
            self.assertNotEqual(tz1, test_tz)

    def test_create_account(self):

        a = Account(self.account_number, self.first_name, self.last_name, self.tz, self.balance)

        self.assertEqual(self.account_number, a.account_number)
        self.assertEqual(self.first_name, a.first_name)
        self.assertEqual(self.last_name, a.last_name)
        self.assertEqual(self.first_name + ' ' + self.last_name, a.full_name)
        self.assertEqual(self.tz, a.timezone)
        self.assertEqual(self.balance, a.balance)

    def test_create_account_blank_first_name(self):
        self.first_name = ' '
        with self.assertRaises(ValueError):
            a = Account(self.account_number, self.first_name, self.last_name)

    def test_create_account_negative_balance(self):
        self.balance = -100
        with self.assertRaises(ValueError):
            a = Account(self.account_number, self.first_name, self.last_name, initial_balance=self.balance)

    def test_account_withdraw_ok(self):
        withdrawal_amount = 20
        a = Account(self.account_number, self.first_name, self.last_name, initial_balance=self.balance)
        conf_code = a.withdraw(withdrawal_amount)
        self.assertTrue(conf_code.startswith('W-'))
        self.assertEqual(self.balance - withdrawal_amount, a.balance)

    def test_account_withdraw_overdrive(self):
        withdrawal_amount = 200
        a = Account(self.account_number, self.first_name, self.last_name, initial_balance=self.balance)
        conf_code = a.withdraw(withdrawal_amount)
        self.assertTrue(conf_code.startswith('X-'))
        self.assertEqual(self.balance, a.balance)


def run_tests(test_class):
    suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


run_tests(TestAccount)
