from db import cusor
import server.config as config
import requests

def create_account(account_number, account_type, in_vault, user_id):
    query = """
        INSERT INTO accounts (account_number, account_type, in_vault, user_id)
        VALUES (%s, %s, %s, %s)
    """
    cusor.execute(query, (account_number, account_type, in_vault, user_id))
    return cusor.lastrowid

def get_account(account_number):
    query = "SELECT * FROM accounts WHERE account_number = %s"
    cusor.execute(query, (account_number,))
    account = cusor.fetchone()
    if not account:
        return None

    if account[3] == 1:
        # If the account is in vault, forward the request to the vault server
        return forward_to_vault_server(account_number)
    
    return {
        'account_number': account[0],
        'account_type': account[1],
        'in_vault': account[2],
        'user_id': account[3],
        "account_status": account[4],
        'balance': account[5],
        'created_at': str(account[6]),
        'updated_at': str(account[7])
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
    # Check if both accounts are in vault
    from_account_data = get_account(from_account)
    to_account_data = get_account(to_account)

    if from_account_data['in_vault'] and to_account_data['in_vault']:
        # Forward the transfer request to the vault server
        return forward_transfer_to_vault_server(from_account, to_account, amount)
    if from_account_data['in_vault']:
        # Move amount from vault to local account
        remove_amount_from_vault(from_account, amount)
        # Then transfer from local account to the destination account
        query = "UPDATE accounts SET balance = balance - %s WHERE account_number = %s"
        cusor.execute(query, (amount, from_account))
        # Check if the transfer was successful
    if to_account_data['in_vault']:
        # Move amount from local account to vault
        add_amount_to_vault(to_account, amount)
        # Then transfer from vault to the destination account
        query = "UPDATE accounts SET balance = balance + %s WHERE account_number = %s"
        cusor.execute(query, (amount, to_account))
        
    return True

def add_amount(account_number, amount):
    # Check if the account is in vault
    account_data = get_account(account_number)
    if account_data['in_vault']:
        # Forward the request to the vault server
        return add_amount_to_vault(account_number, amount)
    else:
        # Update the local account balance
        query = "UPDATE accounts SET balance = balance + %s WHERE account_number = %s"
        cusor.execute(query, (amount, account_number))
        return True