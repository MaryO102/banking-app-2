import unittest
from bank_account import BankAccount

class TestBankAccount(unittest.TestCase):

    def setUp(self):
        """Create a test account before each test."""
        self.account = BankAccount("Jane Doe", 500)

    def test_deposit(self):
        self.account.deposit(200)
        self.assertEqual(self.account.get_balance(), 700)

    def test_withdraw(self):
        self.account.withdraw(100)
        self.assertEqual(self.account.get_balance(), 400)

    def test_withdraw_insufficient_funds(self):
        self.account.withdraw(600)
        self.assertEqual(self.account.get_balance(), 500)

    def test_invalid_deposit(self):
        self.account.deposit(-50)
        self.assertEqual(self.account.get_balance(), 500)

    def test_invalid_withdrawal(self):
        self.account.withdraw(-30)
        self.assertEqual(self.account.get_balance(), 500)

if __name__ == '__main__':
    unittest.main()
