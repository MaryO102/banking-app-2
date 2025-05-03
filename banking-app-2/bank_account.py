# bank-account.py
import mysql.connector

# Connect to MySQL database
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Use your MySQL username
        password="your_mysql_password",  # Use your MySQL password
        database="banking_system"
    )

# Create the accounts table
def initialize_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            account_number INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(100) NOT NULL,
            pin VARCHAR(10) NOT NULL,
            balance DOUBLE DEFAULT 0.0,
            is_admin BOOLEAN DEFAULT FALSE
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()

# Add a new user or admin
def create_account(name, pin, is_admin=False):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO accounts (name, pin, is_admin) VALUES (%s, %s, %s)",
        (name, pin, is_admin)
    )
    conn.commit()
    print(f"Account created for {name}")
    cursor.close()
    conn.close()

# Check if the account and PIN match an existing user
def authenticate(account_number, pin):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM accounts WHERE account_number = %s AND pin = %s",
        (account_number, pin)
    )
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

# Delete a user account
def delete_account(account_number):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM accounts WHERE account_number = %s", (account_number,))
    conn.commit()
    cursor.close()
    conn.close()

# Modify user details (name or PIN)
def modify_account(account_number, new_name=None, new_pin=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if new_name:
        cursor.execute("UPDATE accounts SET name = %s WHERE account_number = %s", (new_name, account_number))
    if new_pin:
        cursor.execute("UPDATE accounts SET pin = %s WHERE account_number = %s", (new_pin, account_number))
    conn.commit()
    cursor.close()
    conn.close()

# BankAccount class for operations tied to a specific user
class BankAccount:
    def __init__(self, account_number):
        self.account_number = account_number
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()

    # Retrieve current account balance
    def get_balance(self):
        self.cursor.execute("SELECT balance FROM accounts WHERE account_number = %s", (self.account_number,))
        result = self.cursor.fetchone()
        return result[0] if result else 0.0

    # Deposit money into account
    def deposit(self, amount):
        if amount <= 0:
            print("Invalid amount.")
            return
        self.cursor.execute("UPDATE accounts SET balance = balance + %s WHERE account_number = %s",
                            (amount, self.account_number))
        self.conn.commit()
        print(f"Deposited ${amount:.2f}")

    # Withdraw money from account
    def withdraw(self, amount):
        self.cursor.execute("SELECT balance FROM accounts WHERE account_number = %s", (self.account_number,))
        balance = self.cursor.fetchone()[0]
        if amount > balance:
            print("Insufficient funds.")
            return
        self.cursor.execute("UPDATE accounts SET balance = balance - %s WHERE account_number = %s",
                            (amount, self.account_number))
        self.conn.commit()
        print(f"Withdrew ${amount:.2f}")

    # Close the connection
    def close(self):
        self.cursor.close()
        self.conn.close()

