from lib.chat import chatroom

class Employee :
    def __init__(self, username, password, privilege, employee_id, email=None, first_name=None, last_name=None, status=None, avatar_url=None):
        self.username = username
        self.password = password
        self.privilege = privilege
        self.employee_id = employee_id
        self.privileges = ['admin', 'user', 'trader']
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.status = status
        self.avatar_url = avatar_url

    def __repr__(self):
        return f"Employee(username={self.username}, privilege={self.privilege}, employee_id={self.employee_id})"

    @staticmethod
    def register(username, password, email, first_name, last_name, avatar_url="/static/images/default_avatar.png"):
        from database.db import do_query
        if not username or not password or not email:
            return None
        if not first_name or not last_name:
            return None
        employee_id = do_query("INSERT INTO Employees (username, password, email, first_name, last_name, avatar_url) VALUES (%s, %s, %s, %s, %s, %s)", (username, password, email, first_name, last_name, avatar_url))
        if not employee_id:
            return None
        return Employee(
            username=username,
            password=password,
            privilege='user',
            employee_id=employee_id,
            email=email,
            first_name=first_name,
            last_name=last_name,
            status='active',
            avatar_url=avatar_url
        )

    @staticmethod
    def get_employee_employee_id(employee_id):
        from database.db import  fetch_row

        employee_data = fetch_row("SELECT * FROM Employees WHERE id = %s", (employee_id,))
        if not employee_data:
            return None
        return Employee(
            username=employee_data['username'],
            password=employee_data['password'],
            privilege=employee_data['privilege'],
            employee_id=employee_data['id'],
            email=employee_data['email'],
            first_name=employee_data['first_name'],
            last_name=employee_data['last_name'],
            status=employee_data['status'],
            avatar_url=employee_data['avatar_url']
        )


    @staticmethod
    def login(username:str| None, password, email:str| None = None):
        from database.db import fetch_row
        if not password:
            return None
        if not username and not email:
            return None
        if username:
            employee_data = fetch_row("SELECT * FROM Employees WHERE username = %s AND password = %s", (username, password))
        elif email:
            employee_data = fetch_row("SELECT * FROM Employees WHERE email = %s AND password = %s", (email, password))
        if not employee_data:
            return None
        return Employee(
            username=employee_data['username'],
            password=employee_data['password'],
            privilege=employee_data['privilege'],
            employee_id=employee_data['id'],
            email=employee_data['email'],
            first_name=employee_data['first_name'],
            last_name=employee_data['last_name'],
            status=employee_data['status'],
            avatar_url=employee_data['avatar_url']
        )


    def update_password(self, new_password):
        from database.db import do_query
        if not new_password:
            raise ValueError("Password cannot be empty.")
        self.password = new_password
        do_query("UPDATE Employees SET password = %s WHERE employee_id = %s", (self.password, self.employee_id))

    def update_privilege(self, new_privilege):
        from database.db import do_query
        if new_privilege not in self.privileges:
            raise ValueError(f"Invalid privilege: {new_privilege}. Must be one of {self.privileges}.")
        self.privilege = new_privilege
        do_query("UPDATE Employees SET privilege = %s WHERE employee_id = %s", (self.privilege, self.employee_id))

    
    def chat(self, message):
        messsage_info = {
            'sender': self.username,
            'sender_id': self.employee_id,
            'message': message
        }
        chatroom.add_message(messsage_info)

    def to_json(self):
        from database.db import fetch_row
        employee_data = fetch_row("SELECT * FROM Employees WHERE id = %s", (self.employee_id,))

        if not employee_data:
            return None

        return {
            'username': employee_data['username'],
            'email': employee_data['email'],
            'first_name': employee_data['first_name'],
            'last_name': employee_data['last_name'],
            'status': employee_data['status'],
            'privilege': employee_data['privilege'],
            'id': employee_data['id'],
            'avatar_url': employee_data['avatar_url'],
            'created_at': str(employee_data['created_at']),
            'updated_at': str(employee_data['updated_at'])
        }

def get_employee_by_id(employee_id):
    from database.db import fetch_row
    employee_data = fetch_row("SELECT * FROM Employees WHERE id = %s", (employee_id,))
    
    if not employee_data:
        return None

    return Employee(
        username=employee_data['username'],
        password=employee_data['password'],
        privilege=employee_data['privilege'],
        employee_id=employee_data['id'],
        email=employee_data['email'],
        first_name=employee_data['first_name'],
        last_name=employee_data['last_name'],
        status=employee_data['status'],
        avatar_url=employee_data['avatar_url']
    )