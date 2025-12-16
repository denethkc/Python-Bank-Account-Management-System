import random
import json
import os
from datetime import datetime

DATA_FILE = "accounts.json"


class BankAccount:
    def __init__(self, account_number, balance=0, transactions=None):
        self.account_number = account_number
        self.balance = balance
        self.transactions = transactions if transactions else []

    def _time(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def deposit(self, amount):
        if amount <= 0:
            return "Amount must be positive"
        self.balance += amount
        self.transactions.append(
            f"{self._time()} | Deposited {amount} | Balance {self.balance}"
        )
        return f"Deposited {amount}. Current balance: {self.balance}"

    def withdraw(self, amount):
        if amount <= 0:
            return "Amount must be positive"
        if amount > self.balance:
            return "Insufficient funds"
        self.balance -= amount
        self.transactions.append(
            f"{self._time()} | Withdrawn {amount} | Balance {self.balance}"
        )
        return f"Withdrew {amount}. Current balance: {self.balance}"

    def transfer(self, amount, target_account):
        result = self.withdraw(amount)
        if result.startswith("Withdrew"):
            target_account.deposit(amount)
            self.transactions.append(
                f"{self._time()} | Transferred {amount} to {target_account.account_number}"
            )
            return f"Transferred {amount} to account {target_account.account_number}"
        return result

    def to_dict(self):
        return {
            "balance": self.balance,
            "transactions": self.transactions
        }


class Bank:
    def __init__(self):
        self.accounts = {}
        self.load_data()

    def generate_account_number(self):
        while True:
            acc_no = ''.join(random.choices('0123456789', k=8))
            if acc_no not in self.accounts:
                return acc_no

    def create_account(self, initial_balance=0):
        acc_no = self.generate_account_number()
        account = BankAccount(acc_no, initial_balance)
        if initial_balance > 0:
            account.transactions.append(
                f"{account._time()} | Account opened with balance {initial_balance}"
            )
        self.accounts[acc_no] = account
        self.save_data()
        return f"Account created successfully!\nAccount Number: {acc_no}"

    def get_account(self, acc_no):
        return self.accounts.get(acc_no)

    def save_data(self):
        data = {acc: obj.to_dict() for acc, obj in self.accounts.items()}
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def load_data(self):
        if not os.path.exists(DATA_FILE):
            return
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            for acc_no, details in data.items():
                self.accounts[acc_no] = BankAccount(
                    acc_no,
                    details["balance"],
                    details["transactions"]
                )


def get_amount(prompt):
    try:
        return float(input(prompt))
    except ValueError:
        print("Please enter a valid number.")
        return None


def main():
    bank = Bank()

    while True:
        print("\n===== Bank Account Management System =====")
        print("1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Check Balance")
        print("5. Transfer Money")
        print("6. View Transaction History")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            amount = get_amount("Enter initial balance: ")
            if amount is not None:
                print(bank.create_account(amount))

        elif choice == '2':
            acc = input("Enter account number: ")
            account = bank.get_account(acc)
            if account:
                amount = get_amount("Enter deposit amount: ")
                if amount is not None:
                    print(account.deposit(amount))
                    bank.save_data()
            else:
                print("Account not found")

        elif choice == '3':
            acc = input("Enter account number: ")
            account = bank.get_account(acc)
            if account:
                amount = get_amount("Enter withdrawal amount: ")
                if amount is not None:
                    print(account.withdraw(amount))
                    bank.save_data()
            else:
                print("Account not found")

        elif choice == '4':
            acc = input("Enter account number: ")
            account = bank.get_account(acc)
            if account:
                print(f"Current balance: {account.balance}")
            else:
                print("Account not found")

        elif choice == '5':
            from_acc = input("Enter your account number: ")
            to_acc = input("Enter target account number: ")
            from_account = bank.get_account(from_acc)
            to_account = bank.get_account(to_acc)
            if from_account and to_account:
                amount = get_amount("Enter transfer amount: ")
                if amount is not None:
                    print(from_account.transfer(amount, to_account))
                    bank.save_data()
            else:
                print("One or both accounts not found")

        elif choice == '6':
            acc = input("Enter account number: ")
            account = bank.get_account(acc)
            if account:
                print("\n--- Transaction History ---")
                print("\n".join(account.transactions) or "No transactions")
            else:
                print("Account not found")

        elif choice == '7':
            print("Thank you! Data saved successfully.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
