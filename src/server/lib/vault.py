import server.config as config
import requests
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
    
def forward_account_to_vault_server(account_number):
    # This function should forward the request to the vault server, creating the account in vault

    url = f"{config.VAULT_SERVER_URL}/accounts/{account_number}"

    response = requests.post(url, timeout=5)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    

def check_vault():
    # This function should check if the vault server is up and running

    url = f"{config.VAULT_SERVER_URL}/health"

    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        return True
    else:
        return False