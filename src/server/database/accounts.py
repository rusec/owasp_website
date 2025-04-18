from random_address.random_address import Dict
import server.config as config
import requests
import server.database.db as db

def create_account(account_number, account_type, in_vault, user_id):
    cursor, sql_db = db.get_cursor()

    query = """
        INSERT INTO accounts (account_number, account_type, in_vault, user_id)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (account_number, account_type, in_vault, user_id))

    lastrowid = cursor.lastrowid
    if not lastrowid:
        return None

    sql_db.commit()
    cursor.close()

    # add to vault server


    return cursor.lastrowid



def get_account_internal(account_number:str):

    cursor, _ = db.get_cursor(dictionary=True)
    query = "SELECT * FROM accounts WHERE account_number = %s"
    cursor.execute(query, (account_number,))
    account = cursor.fetchone()

    if not account :
        return None

    if type(account) != Dict:
        return None

    cursor.close()

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
    cursor, _ = db.get_cursor(dictionary=True)

    query = "SELECT * FROM accounts WHERE account_number = %s"
    cursor.execute(query, (account_number,))
    account = cursor.fetchone()
    if not account:
        return None

    if type(account) != Dict:
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

def forward_to_vault_server(account_number):
    # This function should forward the request to the vault server

    url = f"{config.VAULT_SERVER_URL}/accounts/{account_number}"

    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def forward_transfer_to_vault_server(from_account, to_account, amount):
    # This function should forward the transfer request to the vault server

    url = f"{config.VAULT_SERVER_URL}/transfer"

    data = {
        'from_account': from_account,
        'to_account': to_account,
        'amount': amount
    }

    response = requests.post(url, json=data, timeout=5)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def add_amount_to_vault(account_number, amount):
    # This function should forward the request to move amount to the vault server

    url = f"{config.VAULT_SERVER_URL}/add_amount"

    data = {
        'account_number': account_number,
        'amount': amount
    }

    response = requests.post(url, json=data, timeout=5)
    if response.status_code == 200:
        return response.json()
    else:
        return None
def remove_amount_from_vault(account_number, amount):
    # This function should forward the request to move amount from the vault server

    url = f"{config.VAULT_SERVER_URL}/del_amount"

    data = {
        'account_number': account_number,
        'amount': amount
    }

    response = requests.post(url, json=data, timeout=5)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def transfer_funds(from_account, to_account, amount):
    """
    Transfer funds between two accounts. If either account is in the vault, forward the request to the vault server.
    Ensure that the user has access to both accounts.
    """

    # Check if both accounts are in vault
    from_account_data = get_account_internal(from_account)
    to_account_data = get_account_internal(to_account)

    if not from_account_data or not to_account_data:
        return False

    if from_account_data['balance'] < amount:
        return False


    if from_account_data['in_vault'] and to_account_data['in_vault']:
        # Forward the transfer request to the vault server
        return forward_transfer_to_vault_server(from_account, to_account, amount)

    cursor, sql_db = db.get_cursor()

    if from_account_data['in_vault']:
        # Move amount from vault to local account
        remove_amount_from_vault(from_account, amount)
        # Then transfer from local account to the destination account
        query = "UPDATE accounts SET balance = balance - %s WHERE account_number = %s"
        cursor.execute(query, (amount, from_account))
        # Check if the transfer was successful
    if to_account_data['in_vault']:
        # Move amount from local account to vault
        add_amount_to_vault(to_account, amount)
        # Then transfer from vault to the destination account
        query = "UPDATE accounts SET balance = balance + %s WHERE account_number = %s"
        cursor.execute(query, (amount, to_account))

    if from_account_data['in_vault'] == 0 and to_account_data['in_vault'] == 0:
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

    return True

def add_amount(account_number, amount):
    # Check if the account is in vault
    account_data = get_account_internal(account_number)
    if not account_data:
        return False

    if account_data['in_vault']:
        # Forward the request to the vault server
        return add_amount_to_vault(account_number, amount)
    else:
        cursor, sql_db = db.get_cursor()
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
