from faker import Faker
import requests
import random
import time
from config import HTTP_URL

def create_user():
    fake = Faker()
    username = fake.user_name()
    password = fake.password()
    email = fake.email()
    first_name = fake.first_name()
    last_name = fake.last_name()
    phone = fake.phone_number()


    user_json = {
        'username': username,
        'password': password,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'phone_number': phone,

    }
    # create user on server
    response = requests.post(f'{HTTP_URL}/api/user/register', json=user_json)
    if response.status_code != 201:
        print(f"Error creating user: {response}")
        return None

    # login to server
    login_json = {
        'username': username,
        'password': password
    }
    response = requests.post(f'{HTTP_URL}/api/user/login', json=login_json)

    if response.status_code != 200:
        print(f"Error logging in: {response}")
        return None
    token = response.headers['Authorization']
    if not token:
        print("Error: No token returned")
        return None

    # get user info
    response = requests.get(f'{HTTP_URL}/api/user/info', headers={'Authorization': token})
    if response.status_code != 200:
        print(f"Error getting user info: {response}")
        return None
    user_info = response.json()
    if not user_info:
        print("Error: No user info returned")
        return None
    user_info.update({
        'headers': {
            'Authorization': token
        }
    })
    return user_info


def create_users(num_users):
    users = []
    for i in range(num_users):
        try:
            user = create_user()
            if not user:
                print("Error: No user returned")
                continue
            users.append(user)
        except Exception as e:
            print(f"Error creating user: {e}")
            continue

    return users

def create_transaction(user_from, user_to, amount=10.0):
    # create transaction on server
    response = requests.post(f'{HTTP_URL}/api/account/transfer', json={
        'account_from': user_from['account_number'],
        'account_to': user_to['account_number'],
        'amount': amount
    }, headers=user_from['headers'])
    if response.status_code != 200:
        print(f"Error creating transaction: {response}")
        return None

    return response.json()


def create_employee():
    fake = Faker()
    username = fake.user_name()
    password = fake.password()
    email = fake.email()
    first_name = fake.first_name()
    last_name = fake.last_name()
    employee_json = {
        'username': username,
        'password': password,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
    }

    # create employee on server
    response = requests.post(f'{HTTP_URL}/api/employee/register', json=employee_json)
    if response.status_code != 201:
        print(f"Error creating employee: {response}")
        return None

    # login to server
    login_json = {
        'username': username,
        'password': password
    }
    response = requests.post(f'{HTTP_URL}/api/employee/login', json=login_json)
    if response.status_code != 200:
        print(f"Error logging in: {response}")
        return None

    token = response.headers['Authorization']
    if not token:
        print("Error: No token returned")
        return None
    # get employee info
    response = requests.get(f'{HTTP_URL}/api/employee/info', headers={'Authorization': token})
    if response.status_code != 200:
        print(f"Error getting employee info: {response}")
        return None
    employee_info = response.json()
    if not employee_info:
        print("Error: No employee info returned")
        return None
    employee_info.update({
        'headers': {
            'Authorization': token
        }
    })
    return employee_info


def create_employees(num_employees):
    employees = []
    for i in range(num_employees):
        try:
            employee = create_employee()
            if not employee:
                print("Error: No employee returned")
                continue
            employees.append(employee)

        except Exception as e:
            print(f"Error creating employee: {e}")
            continue

    return employees

def create_employee_chat(employee, message):
    # create chat on server
    response = requests.post(f'{HTTP_URL}/api/chat/publish', json={
        'message': message
    }, headers=employee['headers'])
    if response.status_code != 200:
        print(f"Error creating chat: {response.json()}")
        return None
    return response.json()

def generate_employee_chat(employee):
    fake = Faker()
    message = fake.sentence()
    response = create_employee_chat(employee, message)
    if not response:
        print("Error creating employee chat")
        return None
    return response


def start_generating():
    employees = create_employees(10)
    users = create_users(50)

    while True:
        try:
            user_from = users[random.randint(0, len(users) - 1)]
            user_to = users[random.randint(0, len(users) - 1)]
            if user_from['account_number'] == user_to['account_number']:
                continue
            amount = random.uniform(1.0, 1000.0)
            create_transaction(user_from, user_to, amount)
            print(f"Transferred {amount} from account {user_from['account_number']} to account {user_to['account_number']}")
            time.sleep(random.randint(1, 5))

            # random employee chat
            employee = employees[random.randint(0, len(employees) - 1)]
            generate_employee_chat(employee)
        except Exception as e:
            print(f"Error generating data: {e}")
            continue


start_generating()
