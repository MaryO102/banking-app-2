# test_bank_account.py
import unittest
from bank_account import *

# Test class for BankAccount features
class TestBankAccount(unittest.TestCase):
    def setUp(self):
        initialize_database()
        create_account("TestUser", "0000")
        self.user = authenticate(1, "0000")
        self.account = BankAccount(self.user[0])

    # Test deposit functionality
    def test_deposit(self):
        self.account.deposit(100)
        self.assertEqual(self.account.get_balance(), 100)

    # Test withdrawal functionality
    def test_withdraw(self):
        self.account.deposit(100)
        self.account.withdraw(40)
        self.assertEqual(self.account.get_balance(), 60)

    # Test trying to withdraw more than balance
    def test_insufficient_withdraw(self):
        self.account.deposit(20)
        self.account.withdraw(50)
        self.assertEqual(self.account.get_balance(), 20)

# Run tests
if __name__ == '__main__':
    unittest.main()
