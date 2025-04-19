from src.server.database.db import do_query, fetch_row
from src.server.lib.chat import chatroom

class Employee :
    def __init__(self, username, password, privilege, employee_id):
        self.username = username
        self.password = password
        self.privilege = privilege
        self.employee_id = employee_id
        self.privileges = ['admin', 'user', 'trader']

    def __repr__(self):
        return f"Employee(username={self.username}, privilege={self.privilege}, employee_id={self.employee_id})"

    @staticmethod
    def login(username, password):
        employee_data = fetch_row("SELECT * FROM Employees WHERE username = %s AND password = %s", (username, password))
        if not employee_data:
            return None
        return Employee(
            username=employee_data['username'],
            password=employee_data['password'],
            privilege=employee_data['privilege'],
            employee_id=employee_data['id']
        )


    def update_password(self, new_password):
        if not new_password:
            raise ValueError("Password cannot be empty.")
        self.password = new_password
        do_query("UPDATE Employees SET password = %s WHERE employee_id = %s", (self.password, self.employee_id))

    def update_privilege(self, new_privilege):
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

    employee_data = fetch_row("SELECT * FROM Employees WHERE id = %s", (employee_id,))

    if employee_data:
        return Employee(
            username=employee_data['username'],
            password=employee_data['password'],
            privilege=employee_data['privilege'],
            employee_id=employee_data['id']
        )
    return None
