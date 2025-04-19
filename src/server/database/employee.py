from db import cursor


def get_employee(username):
    query = "SELECT * FROM Employees WHERE username = %s"
    cursor.execute(query, (username,))
    employee = cursor.fetchone()

    if not employee:
        return None

    (id, username, password, email, first_name, last_name, status, privilege, avatar_url, created_at, updated_at) = employee

    return {
        'id': id,
        'username': username,
        # 'password': password,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'status': status,
        'privilege': privilege,
        'avatar_url': avatar_url,
        'created_at': str(created_at),
        'updated_at': str(updated_at)
    }


def get_employee_by_id(employee_id):
    query = "SELECT * FROM Employees WHERE id = %s"
    cursor.execute(query, (employee_id,))
    employee = cursor.fetchone()

    if not employee:
        return None

    (id, username, password, email, first_name, last_name, status, privilege, avatar_url, created_at, updated_at) = employee

    return {
        'id': id,
        'username': username,
        # 'password': password,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'status': status,
        'privilege': privilege,
        'avatar_url': avatar_url,
        'created_at': str(created_at),
        'updated_at': str(updated_at)
    }


def create_employee(username, password, email, first_name, last_name, avatar_url="/static/images/default_avatar.png"):
    query = """
        INSERT INTO Employees (username, password, email, first_name, last_name, avatar_url)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (username, password, email, first_name, last_name, avatar_url))
    return cursor.lastrowid

def update_privilege(user_id: int, privilege: str):
    allows_privilege = ['admin', 'user', 'trader']
    if privilege not in allows_privilege:
        return False

    query = "UPDATE Employees SET privilege = %s WHERE user_id = %s"
    cursor.execute(query, (privilege, user_id))
    if cursor.rowcount > 0:
        return True
    else:
        return False

def update_password(user_id: int, new_password: str):
    query = "UPDATE Employees SET password = %s WHERE user_id = %s"
    cursor.execute(query, (new_password, user_id))
    if cursor.rowcount > 0:
        return True
    else:
        return False
