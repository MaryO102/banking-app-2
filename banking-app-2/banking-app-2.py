import sqlite3

class BankAccount:
    def __init__(self, user_id):
        self.user_id = user_id
        # Connect to a local database file (created automatically if it doesn't exist)
        self.conn = sqlite3.connect('bank.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        #table for storing account balances
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                user_id TEXT PRIMARY KEY,
                balance REAL DEFAULT 0.0
            )
        ''')

        #table to track deposits and withdrawals
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                amount REAL,
                type TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        self.conn.commit()

    def create_account(self):
        # create account if it doesn't exist already
        self.cursor.execute(
            'INSERT OR IGNORE INTO accounts (user_id, balance) VALUES (?, ?)',
            (self.user_id, 0.0)
        )
        self.conn.commit()

    def deposit(self, amount):
        # Add money to the account
        self.cursor.execute(
            'UPDATE accounts SET balance = balance + ? WHERE user_id = ?',
            (amount, self.user_id)
        )
        # Save transaction
        self.cursor.execute(
            'INSERT INTO transactions (user_id, amount, type) VALUES (?, ?, ?)',
            (self.user_id, amount, 'deposit')
        )
        self.conn.commit()

    def withdraw(self, amount):
        # Check balance before withdrawing
        current_balance = self.get_balance()
        if amount <= current_balance:
            self.cursor.execute(
                'UPDATE accounts SET balance = balance - ? WHERE user_id = ?',
                (amount, self.user_id)
            )
            self.cursor.execute(
                'INSERT INTO transactions (user_id, amount, type) VALUES (?, ?, ?)',
                (self.user_id, amount, 'withdraw')
            )
            self.conn.commit()
        else:
            print("Insufficient funds.")

    def get_balance(self):
        # Look up balance from the accounts table
        self.cursor.execute(
            'SELECT balance FROM accounts WHERE user_id = ?',
            (self.user_id,)
        )
        result = self.cursor.fetchone()
        return result[0] if result else 0.0