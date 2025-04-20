import config as config
import requests

def forward_to_vault_server(account_number):
    # This function should forward the request to the vault server

    url = f"{config.VAULT_SERVER_URL}/api/account/{account_number}"

    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    

def forward_transfer_to_vault_server(from_account, to_account, amount):
    # This function should forward the transfer request to the vault server

    url = f"{config.VAULT_SERVER_URL}/api/account/transfer"

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

    url = f"{config.VAULT_SERVER_URL}/api/account/add_amount"

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

    url = f"{config.VAULT_SERVER_URL}/api/account/del_amount"

    data = {
        'account_number': account_number,
        'amount': amount
    }

    response = requests.post(url, json=data, timeout=5)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
def forward_account_to_vault_server(account_number):
    # This function should forward the request to the vault server, creating the account in vault

    url = f"{config.VAULT_SERVER_URL}/api/account/{account_number}"

    response = requests.post(url, timeout=5)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    

def check_vault():
    # This function should check if the vault server is up and running
    try:
        url = f"{config.VAULT_SERVER_URL}/health"

        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        # Handle the exception (e.g., log it, return an error message, etc.)
        print(f"Error connecting to vault server: {e}")
        return False