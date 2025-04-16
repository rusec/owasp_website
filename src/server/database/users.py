from db import cusor
import utils
import accounts


def get_user(username):
    query = "SELECT * FROM users WHERE username = %s"
    cusor.execute(query, (username,))
    user = cusor.fetchone()
    if user:
        return {
            'id': user[0],
            'username': user[1],
            # 'password': user[2],
            'email': user[3],
            'first_name': user[4],
            'last_name': user[5],
            'phone': user[6],
            'address': user[7],
            'city': user[8],
            'state': user[9],
            'zip': user[10],
            'country': user[11],
            'status': user[12],
            'account_number': user[13],
            'created_at': str(user[14]),
            'updated_at': str(user[15])
        }
    else:
        return None

def get_user_by_id(user_id):
    query = "SELECT * FROM users WHERE id = %s"
    cusor.execute(query, (user_id,))
    user = cusor.fetchone()
    if user:
        return {
            'id': user[0],
            'username': user[1],
            # 'password': user[2],
            'email': user[3],
            'first_name': user[4],
            'last_name': user[5],
            'phone': user[6],
            'address': user[7],
            'city': user[8],
            'state': user[9],
            'zip': user[10],
            'country': user[11],
            'status': user[12],
            'account_number': user[13],
            'created_at': str(user[14]),
            'updated_at': str(user[15])
        }
    else:
        return None
    
def register_user(username, password, email, first_name, last_name, phone, address, city, state, zip, country):


    def delete_user(user_id):
        query = "DELETE FROM users WHERE id = %s"
        cusor.execute(query, (user_id,))
        return cusor.rowcount > 0

    query = """
        INSERT INTO users (username, password, email, first_name, last_name, phone, address, city, state, zip, country)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    cusor.execute(query, (username, password, email, first_name, last_name, phone, address, city, state, zip, country))

    user_id = cusor.lastrowid
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
    cusor.execute(query, (account_number, user_id))
    if cusor.rowcount == 0:
        delete_user(user_id)
        return None

    return cusor.lastrowid

def create_user_account(user_id):
    account_number = utils.generate_account_number()
    account_type = 'savings'
    in_vault = False
    account_status = 'active'
    balance = 0.00

    query = """
        SELECT * FROM accounts WHERE account_number = %s
    """
    cusor.execute(query, (account_number,))
    account = cusor.fetchone()
    if account:
        # If the account already exists, generate a new account number
        return create_user_account(user_id)


    query = """
        INSERT INTO accounts (account_number, account_type, in_vault, account_status, balance, user_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cusor.execute(query, (account_number, account_type, in_vault, account_status, balance, user_id))
    if not cusor.lastrowid:
        return None
    return account_number



