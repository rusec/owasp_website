from db import get_cursor
def login_user(username, password):

    cursor, _ = get_cursor(dictionary=True)
    # Check if the user exists in the database

    # passwords are stored as plain text, given A07:2021 – Identification and Authentication Failures
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    cursor.close()

    if user:
        return True
    else:
        return False

def login_employee(username, password):
    # Check if the employee exists in the database
    cursor, _ = get_cursor(dictionary=True)

    # passwords are stored as plain text, given A07:2021 – Identification and Authentication Failures
    cursor.execute("SELECT * FROM Employees WHERE username = %s AND password = %s", (username, password))
    employee = cursor.fetchone()
    cursor.close()
    if employee:
        return True
    else:
        return False
