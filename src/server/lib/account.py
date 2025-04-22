from database.accounts import get_account_internal, transfer_funds,get_account

from lib.vault import forward_account_to_vault_server

class Account:
    def __init__(self, account_number, user_id, balance):
        self.account_number = int(account_number)
        self.user_id = user_id
        self.balance = balance

    def get_balance(self):
        from database.db import fetch_row
        account = fetch_row("SELECT balance FROM accounts WHERE account_number = %s", (self.account_number,))
        return account['balance'] if account else None

    def transfer_funds(self, to_account_number, amount):
        return transfer_funds(self.account_number, to_account_number, amount)

    def transfer_to_vault(self):
        """
        Transfer the account to the vault server.
        """
        from database.db import do_query
        # Check if the account is already in the vault
        account = get_account_internal(self.account_number)
        if not account:
            return None

        if account.get('in_vault', 0) == 1:
            return None

        # Transfer the account to the vault server

        result = forward_account_to_vault_server(self.account_number, self.balance)
        if not result:
            return None

        result = do_query("UPDATE accounts SET in_vault = 1 WHERE account_number = %s", (self.account_number,))
        return result


    @staticmethod
    def create_account(account_number,user_id, account_type, in_vault):
        """
        DONT USE THIS TO MAKE ACCOUNTS, AN ACCOUNT IS MADE WHEN A USER IS MADE
        """
        from database.db import insert_query
        account = insert_query("""
        INSERT INTO accounts (account_number, account_type, in_vault, user_id)
        VALUES (%s, %s, %s, %s)
        """, (account_number, account_type, in_vault, user_id))

        return account
    @staticmethod
    def get_account(account_number, user_id):
        account = get_account(account_number, user_id)
        if not account:
            return None
        return Account(account['account_number'], account['user_id'], account['balance'])

    def get_transactions(self):
        from database.db import fetch_all
        transactions = fetch_all("SELECT * FROM transactions WHERE account_number = %s", (self.account_number,))
        return transactions if transactions else None

    def to_json(self):
        account = get_account_internal(self.account_number)
        if not account:
            return None
        return account
