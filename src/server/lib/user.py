from src.server.database.db import fetch_row, get_cursor
from src.server.database.users import register_user
from account import Account
class User:
    def __init__(self, username: str, password: str, user_id: int | None = None):
        self.username = username
        self.password = password
        self.id = user_id


    def get_account(self):
        user = self.to_json()
        if not user:
            return None
        account_number = user['account_number']
        return Account.get_account(account_number, self.id)

    @staticmethod
    def register(username: str, password: str, email: str, first_name: str, last_name: str, phone: str, address: str, city: str, state: str, zip_code: str, country: str):
        result = register_user(username, password, email, first_name, last_name, phone, address, city, state, zip_code, country)
        if not result:
            return None

        user_id, account_number = result
        if not account_number or not user_id:
            return None

        return User(username, password, user_id)

    @staticmethod
    def login(username: str, password: str):

        user_data = fetch_row("SELECT * FROM Users WHERE username = %s AND password = %s", (username, password))

        if user_data:
            return User(username, password, user_data['id'])
        return None



    def to_json(self):

        user_data = fetch_row("SELECT * FROM Users WHERE id = %s", (self.id,))

        if not user_data:
            return None

        return{
            'id': user_data['id'],
            'username': user_data['username'],
            # 'password': password,
            'email': user_data['email'],
            'first_name': user_data['first_name'],
            'last_name': user_data['last_name'],
            'phone': user_data['phone'],
            'address': user_data['address'],
            'city': user_data['city'],
            'state': user_data['state'],
            'zip': user_data['zip'],
            'country': user_data['country'],
            'status': user_data['status'],
            'account_number': user_data['account_number'],
            'created_at': str(user_data['created_at']),
            'updated_at': str(user_data['updated_at'])
        }


def get_user_by_id(user_id: int):


    user_data = fetch_row("SELECT * FROM Users WHERE id = %s", (user_id,))

    if user_data:
        return User(
            username=user_data['username'],
            password=user_data['password'],
            user_id=user_data['id']
        )
    return None
