from src.server.database.accounts import get_account_internal, create_account, transfer_funds,get_account
from src.server.database.db import get_cursor
class Account:
    def __init__(self, account_number, user_id, balance):
        self.account_number = account_number
        self.user_id = user_id
        self.balance = balance

    def get_balance(self):
        cursor, _ = get_cursor()
        cursor.execute("SELECT balance FROM accounts WHERE account_number = %s", (self.account_number,))
        balance = cursor.fetchone()
        cursor.close()
        return balance['balance'] if balance else None

    def transfer_funds(self, to_account_number, amount):
        return transfer_funds(self.account_number, to_account_number, amount)

    @staticmethod
    def create_account(account_number,user_id, account_type, in_vault):
        """
        DONT USE THIS TO MAKE ACCOUNTS, AN ACCOUNT IS MADE WHEN A USER IS MADE
        """
        return create_account(account_number, account_type, in_vault, user_id)
    @staticmethod
    def get_account(account_number, user_id):
        account = get_account(account_number, user_id)
        if not account:
            return None
        return Account(account['account_number'], account['user_id'], account['balance'])


    def to_json(self):
        account = get_account_internal(self.account_number)
        if not account:
            return None
        return account
