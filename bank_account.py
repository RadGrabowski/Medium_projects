from datetime import timedelta, datetime
import numbers
import itertools
from collections import namedtuple

"""The project is a simulation of a bank account where you can deposit and withdraw money.
After each transaction an unique code is generated based on the time, account number, and type of operation. You can also get your interest paid based on the adjustable interest rate"""

Confirmation = namedtuple('Confirmation', 'account_number transaction_code transaction_id time_utc time')


class Timezone:
    def __init__(self, name, hours_offset, minutes_offset=0):
        if name is None or len(str(name).strip()) == 0:
            raise ValueError('Timezone name cannot be empty.')
        self._name = str(name).strip()

        if not isinstance(hours_offset, numbers.Integral):
            raise ValueError('Hour offset must be an integer.')

        if not isinstance(minutes_offset, numbers.Integral):
            raise ValueError('Minute offset must be an integer')

        if minutes_offset > 59 or minutes_offset < -59:
            raise ValueError('Minute offset must be between -59 and 59 (inclusive).')

        offset = timedelta(hours=hours_offset, minutes=minutes_offset)
        if offset < timedelta(hours=-12, minutes=0) or offset > timedelta(hours=14, minutes=0):
            raise ValueError('Offset must be between -12:00 and +14:00.')

        self._hours_offset = hours_offset
        self._minutes_offset = minutes_offset
        self._offset = offset

    @property
    def offset(self):
        return self._offset

    @property
    def name(self):
        return self._name

    def __eq__(self, other):
        return (isinstance(other, Timezone) and
                self.name == other.name and
                self._hours_offset == other._hours_offset and
                self._minutes_offset == other._minutes_offset)

    def __repr__(self):
        return (f"Timezone(name={self.name}, "
                f"hours_offset={self._hours_offset},"
                f" minutes_offset={self._minutes_offset}")


class Account:
    transaction_counter = itertools.count(100)
    _interest_rate = 0.5
    _transaction_codes = {'deposit': 'D', 'withdraw': 'W', 'interest': 'I', 'rejected': 'X'}

    def __init__(self, account_number, first_name, last_name, timezone=None, initial_balance=0):
        self._account_number = account_number
        self.first_name = first_name
        self._last_name = last_name

        if timezone is None:
            timezone = Timezone('UTC', 0, 0)
        self._timezone = timezone
        self._balance = Account.validate_real_number(initial_balance, min_value=0)

    @property
    def account_number(self):
        return self._account_number

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self._first_name = Account.validate_name(value, 'First name')

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        self._last_name = Account.validate_name(value, 'Last name')

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def timezone(self):
        return self._timezone

    @timezone.setter
    def timezone(self, value):
        if not isinstance(value, Timezone):
            raise ValueError('Time zone must be a valid Timezone object.')
        self._timezone = value

    @property
    def balance(self):
        return self._balance

    @classmethod
    def get_interest_name(cls):
        return cls._interest_rate

    @classmethod
    def set_interest_name(cls, value):
        if not isinstance(value, numbers.Real):
            raise ValueError('Interest rate must be a real number')
        if value < 0:
            raise ValueError('Interest rate cannot be negative')
        cls._interest_rate = value

    @staticmethod
    def validate_real_number(value, min_value=None):
        if not isinstance(value, numbers.Real):
            raise ValueError('Value must be a real number')
        if min_value is not None and value < min_value:
            raise ValueError(f'Value must be at least {min_value}.')
        return value

    def confirmation_code(self, transaction_code):
        dt_str = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        return f'{transaction_code}-{self.account_number}-{dt_str}-{next(Account.transaction_counter)}'

    @staticmethod
    def validate_name(value, field_title):
        if value is None or len(str(value).strip()) == 0:
            raise ValueError(f'{field_title} cannot be empty')
        return str(value).strip()

    @staticmethod
    def parse_confirmation_code(confirmation_code, preferred_timezone=None):
        parts = confirmation_code.split('-')
        if len(parts) != 4:
            raise ValueError('Invalid confirmation code')

        transaction_code, account_number, raw_dt_utc, transaction_id = parts

        try:
            dt_utc = datetime.strptime(raw_dt_utc, '%Y%m%d%H%M%S')
        except ValueError as ex:
            raise ValueError('Invalid transaction datetime') from ex

        if preferred_timezone is None:
            preferred_timezone = Timezone('UTC', 0, 0)

        if not isinstance(preferred_timezone, Timezone):
            raise ValueError('Invalid timezone specified.')

        dt_preferred = dt_utc + preferred_timezone.offset
        dt_preferred_str = f"{dt_preferred.strftime('%Y-%m-%d %H:%M:%S')} ({preferred_timezone.name()})"

        return Confirmation(account_number, transaction_code, transaction_id, dt_utc.isoformat(), dt_preferred_str)

    def deposit(self, value):
        value = Account.validate_real_number(value, 0.01)
        transaction_code = Account._transaction_codes['deposit']
        conf_code = self.confirmation_code(transaction_code)
        self._balance += value
        return conf_code

    def withdraw(self, value):
        value = Account.validate_real_number(value, 0.01)
        accepted = False
        if self.balance - value < 0:
            transaction_code = Account._transaction_codes['rejected']
        else:
            accepted = True
            transaction_code = Account._transaction_codes['withdraw']

        conf_code = self.confirmation_code(transaction_code)
        if accepted:
            self._balance -= value
        return conf_code

    def pay_interest(self):
        interest = self.balance * Account.get_interest_name() / 100
        conf_code = self.confirmation_code(Account._transaction_codes['interest'])
        self._balance += interest
        return conf_code


if __name__ == '__main__':
    a = Account('A100', 'Eric', 'Idle', initial_balance=-100)
    print(a.balance)

    try:
        print(a.deposit(100))
        print(a.withdraw(200))
        print(a.deposit(100))
        print(a.withdraw(200))
        print(a.balance)
    except ValueError as ex:
        print(ex)
