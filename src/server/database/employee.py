from db import cusor


def get_employee(username):
    query = "SELECT * FROM Employees WHERE username = %s"
    cusor.execute(query, (username,))
    employee = cusor.fetchone()
    if employee:
        return {
            'id': employee[0],
            'username': employee[1],
            'password': employee[2],
            'email': employee[3],
            'first_name': employee[4],
            'last_name': employee[5],
            'status': employee[6],
            'privilege': employee[7],
            'created_at': str(employee[8]),
            'updated_at': str(employee[9])
        }
    else:
        return None

def create_employee(username, password, email, first_name, last_name):
    query = """
        INSERT INTO Employees (username, password, email, first_name, last_name)
        VALUES (%s, %s, %s, %s, %s)
    """
    cusor.execute(query, (username, password, email, first_name, last_name))
    return cusor.lastrowid

def update_privilege(username, privilege):
    allows_privilege = ['admin', 'user', 'trader']
    if privilege not in allows_privilege:
        return False

    query = "UPDATE Employees SET privilege = %s WHERE username = %s"
    cusor.execute(query, (privilege, username))
    if cusor.rowcount > 0:
        return True
    else:
        return False

def update_password(username, new_password):
    query = "UPDATE Employees SET password = %s WHERE username = %s"
    cusor.execute(query, (new_password, username))
    if cusor.rowcount > 0:
        return True
    else:
        return False

