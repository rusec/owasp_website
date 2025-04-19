import random
from db import get_cursor
import utils


def get_user_by_id(user_id):

    cursor, _ = get_cursor(dictionary=True)
    query = "SELECT * FROM users WHERE id = %s"
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()
    if not user:
        return None

    (id, username, password, email, first_name, last_name, phone, address, city, state, zip, country, status, account_number, created_at, updated_at) = user

    cursor.close()
    return {
        'id': id,
        'username': username,
        # 'password': password,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'phone': phone,
        'address': address,
        'city': city,
        'state': state,
        'zip': zip,
        'country': country,
        'status': status,
        'account_number': account_number,
        'created_at': str(created_at),
        'updated_at': str(updated_at)
    }

def register_user(username, password, email, first_name, last_name, phone, address, city, state, zip, country):

    cursor, sql_db = get_cursor(dictionary=True)

    def delete_user(user_id):
        query = "DELETE FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        sql_db.commit()
        rowcount = cursor.rowcount
        cursor.close()
        if rowcount == 0:
            return None
        return rowcount

    query = """
        INSERT INTO users (username, password, email, first_name, last_name, phone, address, city, state, zip, country)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(query, (username, password, email, first_name, last_name, phone, address, city, state, zip, country))

    user_id = cursor.lastrowid
    if not user_id:
        return None
    # Create a new account for the user
    account_number = create_user_account(user_id)
    if not account_number:
        delete_user(user_id)
        return None

    # Update the user's account number in the database
    query = """
        UPDATE users SET account_number = %s WHERE id = %s
    """
    cursor.execute(query, (account_number, user_id))
    if cursor.rowcount == 0:
        delete_user(user_id)
        return None

    # Commit the changes to the database
    sql_db.commit()
    cursor.close()

    return user_id, account_number

def create_user_account(user_id):
    account_number = utils.generate_account_number()
    account_type = 'savings'
    in_vault = False
    account_status = 'active'
    balance = random.uniform(1000, 10000)
    cursor, _ = get_cursor(dictionary=True)
    query = """
        SELECT * FROM accounts WHERE account_number = %s
    """
    cursor.execute(query, (account_number,))
    account = cursor.fetchone()
    if account:
        # If the account already exists, generate a new account number
        return create_user_account(user_id)
    cursor.close()
    # Create a new account for the user
    cursor, sql_db = get_cursor(dictionary=True)

    query = """
        INSERT INTO accounts (account_number, account_type, in_vault, account_status, balance, user_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (account_number, account_type, in_vault, account_status, balance, user_id))
    if not cursor.lastrowid:
        cursor.close()
        return None
    sql_db.commit()
    cursor.close()
    return account_number
