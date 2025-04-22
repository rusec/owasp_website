from random_address.random_address import Dict
from lib.vault import forward_to_vault_server, forward_transfer_to_vault_server, add_amount_to_vault, remove_amount_from_vault


def get_account_internal(account_number:int):
    from database.db import fetch_row
    account = fetch_row("SELECT * FROM accounts WHERE account_number = %s", (account_number,))

    if not account :
        return None

    if account == 1:
        # If the account is in vault, forward the request to the vault server
        return forward_to_vault_server(account_number)

    return {
            "account_number": str(account["account_number"]),
            "account_type": str(account["account_type"]),
            "user_id": str(account["user_id"]),
            "account_status": str(account["account_status"]),
            "balance": str(account["balance"]),
            "created_at": str(account["created_at"]),
            "updated_at": str(account["updated_at"])
        }

def get_account(account_number:str, requested_user_id:str):
    """
    Fetch account information if user is authorized and account is not in vault.
    """
    from database.db import fetch_row

    account = fetch_row("SELECT * FROM accounts WHERE account_number = %s", (account_number,))

    if not account:
        return None

    # doesn't check if user id matches the account for vault accounts, vault assume authentication is done by this server
    if account['in_vault'] == 1:
        # If the account is in vault, forward the request to the vault server
        return forward_to_vault_server(account_number)

    if account['user_id'] != requested_user_id:
        # If the requested user ID does not match the account's user ID, return None
        return None


    return {
        "account_number": str(account["account_number"]),
        "account_type": str(account["account_type"]),
        "user_id": str(account["user_id"]),
        "account_status": str(account["account_status"]),
        "balance": str(account["balance"]),
        "created_at": str(account["created_at"]),
        "updated_at": str(account["updated_at"])
    }


def transfer_funds(from_account, to_account, amount):
    """
    Transfer funds between two accounts. If either account is in the vault, forward the request to the vault server.
    Ensure that the user has access to both accounts.
    """
    from database.db import get_cursor
    # Check if both accounts are in vault
    from_account_data = get_account_internal(from_account)
    to_account_data = get_account_internal(to_account)

    if not from_account_data or not to_account_data:
        return False

    if float(from_account_data['balance']) < amount:
        return False


    if from_account_data.get('in_vault', 0) == 1 and to_account_data.get('in_vault', 0) == 1:
        # Forward the transfer request to the vault server
        result =  forward_transfer_to_vault_server(from_account, to_account, amount)
        if not result:
            return False

        log_transfer(from_account, to_account, amount)

        return True

    cursor, sql_db = get_cursor()

    if from_account_data.get('in_vault', 0) == 1:
        # Move amount from vault to local account
        remove_amount_from_vault(from_account, amount)
        # Then transfer from local account to the destination account
        query = "UPDATE accounts SET balance = balance - %s WHERE account_number = %s"
        cursor.execute(query, (amount, from_account))
        # Check if the transfer was successful
    if to_account_data.get('in_vault', 0) == 1:
        # Move amount from local account to vault
        add_amount_to_vault(to_account, amount)
        # Then transfer from vault to the destination account
        query = "UPDATE accounts SET balance = balance + %s WHERE account_number = %s"
        cursor.execute(query, (amount, to_account))

    if from_account_data.get('in_vault', 0) == 0 and to_account_data.get('in_vault', 0) == 0:
        # Both accounts are local
        query = "UPDATE accounts SET balance = balance - %s WHERE account_number = %s"
        cursor.execute(query, (amount, from_account))
        query = "UPDATE accounts SET balance = balance + %s WHERE account_number = %s"
        cursor.execute(query, (amount, to_account))

    # Check if the transfer was successful
    if cursor.rowcount == 0:
        return False

    # Commit the changes
    sql_db.commit()
    cursor.close()

    # log the transfer

    result = log_transfer(from_account, to_account, amount)
    if not result:
        return False


    return True

def log_transfer(from_account, to_account, amount):

    # add withdrawal to transaction log

    query = """
        INSERT INTO transactions (account_number, transaction_type, amount, timestamp)
        VALUES (%s, %s, %s, NOW())
    """
    from database.db import insert_query
    result_query = insert_query(query, (from_account, 'withdrawal', amount))
    result_query = insert_query(query, (to_account, 'deposit', amount))
    if not result_query:
        return False
    return True



def add_amount(account_number, amount):
    # Check if the account is in vault
    from database.db import get_cursor
    account_data = get_account_internal(account_number)
    if not account_data:
        return False

    if account_data.get('in_vault', 0) == 1:
        # Forward the request to the vault server
        return add_amount_to_vault(account_number, amount)
    else:
        cursor, sql_db = get_cursor()
        # Update the local account balance
        query = "UPDATE accounts SET balance = balance + %s WHERE account_number = %s"
        cursor.execute(query, (amount, account_number))
        # Check if the update was successful
        if cursor.rowcount == 0:
            return False
        # Commit the changes
        sql_db.commit()
        cursor.close()
        return True
