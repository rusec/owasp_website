from vault.database.db import fetch_row, do_query

class Account():
    def __init__(self, account_number, balance):
        self.account_number = account_number
        self.balance = balance

    @staticmethod
    def create_account(account_number, balance):
        """
        Create a new account with the given account number and balance.
        """
        query = "INSERT INTO accounts (account_number, balance) VALUES (%s, %s)"
        do_query(query, (account_number, balance))
        return Account(account_number, balance)

    @staticmethod
    def get_account(account_number):
        account = fetch_row("SELECT * FROM accounts WHERE account_number = %s", (account_number,))
        if not account:
            return None
        return Account(account['account_number'], account['balance'])
    
    def add_balance(self, amount):
        self.balance += amount
        # Update the balance in the database
        query = "UPDATE accounts SET balance = balance + %s WHERE account_number = %s"
        result = do_query(query, (amount, self.account_number))
        return self.balance if result else None
    
    def remove_balance(self, amount):
        if amount > self.balance:
            return None
        self.balance -= amount
        # Update the balance in the database
        query = "UPDATE accounts SET balance = balance - %s WHERE account_number = %s"
        result = do_query(query, (amount, self.account_number))
        return self.balance if result else None
    
    def get_balance(self):
        return self.balance
    
    def to_json(self):
        account = fetch_row("SELECT * FROM accounts WHERE account_number = %s", (self.account_number,))
        if not account:
            return None
        return {
            "account_number": str(account["account_number"]),
            "balance": str(account["balance"]),
            "accont_type": "valuted",
            "created_at": str(account["created_at"]),
            "updated_at": str(account["updated_at"])
        }