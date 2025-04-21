from app import app
import pytest
from faker import Faker
import random_address

import jwt_utils
@pytest.fixture()
def client ():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'</body></html>' in response.data

def test_register(client):
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

    response = client.post('/api/user/register', json=user_json)
    assert response.status_code == 201

def test_login(client):
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

    client.post('/api/user/register', json=user_json)

    login_json = {
        'username': username,
        'password': password
    }

    response = client.post('/api/user/login', json=login_json)
    assert response.status_code == 200
    assert response.headers['Authorization'] is not None
    assert response.headers['Authorization'] != ''
    assert response.headers['Authorization'] != 'Bearer '

def test_get_user_info(client):
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

    client.post('/api/user/register', json=user_json)

    login_json = {
        'username': username,
        'password': password
    }

    response = client.post('/api/user/login', json=login_json)
    token = response.headers['Authorization']

    headers = {
        'Authorization': token
    }
    jwt_decode = jwt_utils.decode(token)
    # Assuming the user ID is 1 for testing purposes

    response = client.get(f'/api/user/{jwt_decode.get('user_id')}', headers=headers)
    print(response.json)
    assert response.status_code == 200
    assert response.json.get('username') == username
    assert response.json.get('email') == email  
    assert response.json.get('first_name') == first_name
    assert response.json.get('last_name') == last_name
    assert response.json.get('phone') == phone
   
    assert response.json.get('account_number') == jwt_decode.get('account_number')
    

def test_get_user_account(client):
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

    client.post('/api/user/register', json=user_json)

    login_json = {
        'username': username,
        'password': password
    }

    response = client.post('/api/user/login', json=login_json)
    token = response.headers['Authorization']

    headers = {
        'Authorization': token
    }

    jwt_decode = jwt_utils.decode(token)
    print(f'/api/account/{jwt_decode.get('account_number')}')
    # Assuming the user ID is 1 for testing purposes
    response = client.get(f'/api/account/{jwt_decode.get('account_number')}', headers=headers)

    print(response.json)
    assert response.status_code == 200

def test_transfer_funds(client):
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

    client.post('/api/user/register', json=user_json)

    login_json = {
        'username': username,
        'password': password
    }

    response = client.post('/api/user/login', json=login_json)
    token = response.headers['Authorization']

    headers = {
        'Authorization': token
    }

    jwt_decode = jwt_utils.decode(token)

    fake = Faker()
    username = fake.user_name()
    password = fake.password()
    email = fake.email()
    first_name = fake.first_name()
    last_name = fake.last_name()
    phone = fake.phone_number()
    user_two_json = {
        'username': username,
        'password': password,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'phone_number': phone,
 
    }
    client.post('/api/user/register', json=user_two_json)
    login_json = {
        'username': username,
        'password': password
    }
    response = client.post('/api/user/login', json=login_json)
    token_two = response.headers['Authorization']
    headers_two = {
        'Authorization': token_two
    }
    jwt_decode_two = jwt_utils.decode(token_two)

    transfer_json = {
        'account_from': jwt_decode.get('account_number'),
        'account_to': jwt_decode_two.get('account_number'),
        'amount': 100.0
    }
    print(transfer_json)
    response = client.post('/api/account/transfer', json=transfer_json, headers=headers)
    print(response.json)
    assert response.status_code == 200

