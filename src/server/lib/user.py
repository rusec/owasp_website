from lib.account import Account

class User:
    def __init__(self, username: str, password: str, user_id: int | None = None, email: str = None, first_name: str = None, last_name: str = None, phone: str = None, address: str = None, city: str = None, state: str = None, zip_code: str = None, country: str = None):
        self.username = username
        self.password = password
        self.id = user_id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.country = country
        self.account_number = None



    def get_account(self):
        user = self.to_json()
        if not user:
            return None
        account_number = user['account_number']
        return Account.get_account(account_number, self.id)

    def update_password(self, new_password: str):
        from database.db import do_query
        if not self.password:
            return None
        if not self.id:
            return None
        result = do_query("UPDATE users SET password = %s WHERE id = %s", (new_password, self.id))
        if not result:
            return None
        return True

    @staticmethod
    def register(username: str, password: str, email: str, first_name: str, last_name: str, phone: str, address: str, city: str, state: str, zip_code: str, country: str):
        from database.users import register_user
        result = register_user(username, password, email, first_name, last_name, phone, address, city, state, zip_code, country)
        if not result:
            return None

        user_id, account_number = result
        if not account_number or not user_id:
            return None

        return User(username, password, user_id)

    @staticmethod
    def login(username: str| None, password: str, email: str = None):
        from database.db import fetch_row

        if not password:
            return None
        if not username and not email:
            return None
        user_data = None
        if username:
            user_data = fetch_row("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        elif email:
            user_data = fetch_row("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))

        if not user_data:
            return None

        return User(user_data['username'], password, user_data['id'], user_data['email'], user_data['first_name'], user_data['last_name'], user_data['phone'], user_data['address'], user_data['city'], user_data['state'], user_data['zip'], user_data['country'])

    @staticmethod
    def get_user_by_id(user_id: int):
        from database.db import fetch_row

        user_data = fetch_row("SELECT * FROM users WHERE id = %s", (user_id,))

        if user_data:
            return User(
                username=str(user_data['username']),
                password=str(user_data['password']),
                user_id=user_data['id']
            )
        return None

    @staticmethod
    def get_user_by_email(email: str):
        from database.db import fetch_row

        user_data = fetch_row("SELECT * FROM users WHERE email = %s", (email,))

        if user_data:
            return User(
                username=user_data['username'],
                password=user_data['password'],
                user_id=user_data['id']
            )
        return None

    def to_json(self):
        from database.db import fetch_row

        user_data = fetch_row("SELECT * FROM users WHERE id = %s", (self.id,))

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
