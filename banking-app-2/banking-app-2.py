# banking_app-2.py
from bank_account import *
from getpass import getpass  # Use getpass so the PIN isn't visible when typed

# Menu shown to regular users
def customer_menu(account_number, name):
    account = BankAccount(account_number)
    while True:
        print(f"\nWelcome, {name}")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Logout")

        choice = input("Choose an option: ")
        if choice == "1":
            print(f"Balance: ${account.get_balance():.2f}")
        elif choice == "2":
            try:
                amount = float(input("Enter amount: "))
                account.deposit(amount)
            except ValueError:
                print("Invalid input.")
        elif choice == "3":
            try:
                amount = float(input("Enter amount: "))
                account.withdraw(amount)
            except ValueError:
                print("Invalid input.")
        elif choice == "4":
            account.close()
            print("Logged out.")
            break
        else:
            print("Invalid option.")

# Menu shown to admins
def admin_menu():
    while True:
        print("\nAdmin Menu")
        print("1. Create Account")
        print("2. Modify Account")
        print("3. Delete Account")
        print("4. Logout")

        choice = input("Choose an option: ")
        if choice == "1":
            name = input("Enter name: ")
            pin = getpass("Set PIN: ")
            create_account(name, pin)
        elif choice == "2":
            try:
                acc = int(input("Enter account number: "))
                new_name = input("New name (leave blank to skip): ")
                new_pin = getpass("New PIN (leave blank to skip): ")
                modify_account(acc, new_name or None, new_pin or None)
                print("Account updated.")
            except ValueError:
                print("Invalid input.")
        elif choice == "3":
            try:
                acc = int(input("Enter account number to delete: "))
                delete_account(acc)
                print("Account deleted.")
            except ValueError:
                print("Invalid input.")
        elif choice == "4":
            print("Logging out...")
            break
        else:
            print("Invalid option.")

# Login prompt for all users
def login():
    try:
        acc_num = int(input("Account number: "))
        pin = getpass("PIN: ")
        if user := authenticate(acc_num, pin):
            name = user[1]
            is_admin = user[4]
            if is_admin:
                print(f"Welcome Admin {name}")
                admin_menu()
            else:
                customer_menu(acc_num, name)
        else:
            print("Invalid credentials.")
    except ValueError:
        print("Invalid input.")

# App entry point
if __name__ == "__main__":
    initialize_database()
    print("Welcome to the Online Banking System")
    while True:
        print("\n1. Login")
        print("2. Exit")
        choice = input("Choose: ")
        if choice == "1":
            login()
        elif choice == "2":
            print("Goodbye.")
            break
        else:
            print("Invalid option.")
