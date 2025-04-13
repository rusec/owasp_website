from db import cusor
def login(username, password):
    # Check if the user exists in the database

    # passwords are stored as plain text, given A07:2021 – Identification and Authentication Failures
    cusor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cusor.fetchone()
    if user:
        return True
    else:
        return False

def login_employee(username, password):
    # Check if the employee exists in the database

    # passwords are stored as plain text, given A07:2021 – Identification and Authentication Failures
    cusor.execute("SELECT * FROM Employees WHERE username = %s AND password = %s", (username, password))
    employee = cusor.fetchone()
    if employee:
        return True
    else:
        return False
    
