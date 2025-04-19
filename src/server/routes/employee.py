from flask import Blueprint, jsonify, request
import jwt_utils
import server.database.employee as employee_db
from server.lib.employee import Employee 
import server.database.login as login_db

employee_bp = Blueprint('employee', __name__, url_prefix='/api/employee')

@employee_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password and type(username) != str and type(password) != str:
        return jsonify({'message': 'Username and password are required!'}), 400

    employee = Employee.login(username, password)
    if not employee:
        return jsonify({'message': 'Employee not found!'}), 404

    # Generate JWT token
    token = jwt_utils.encode({
        'username': employee['username'] ,
        'privilege': employee['privilege'] ,
        'employee_id': employee['id'],
        'email': employee['email'],
        'first_name': employee['first_name'],
        'last_name': employee['last_name'],
        'status': employee['status'],
        'avatar_url': employee['avatar_url'],
        'role': 'employee',
    })

    request.headers['Authorization'] = f'Bearer {token}'
    request.cookies['Authorization'] = f'Bearer {token}'

    return jsonify({'token': token}), 200

def check_employee_login():
    # Check if the user is logged in
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({'message': 'Unauthorized!'}), 401
    try:
        payload = jwt_utils.decode(token)

        role = payload['role']
        if role != 'employee':
            return jsonify({'message': 'Unauthorized!'}), 401

        return payload
    except jwt_utils.jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expired!'}), 401
    except jwt_utils.jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token!'}), 401

@employee_bp.route('/', methods=['GET'])
@employee_bp.route('/<int:employee_id>', methods=['GET'])
def get_employee():
    payload = check_employee_login()
    if type(payload) != dict:
        return payload
    username = payload['employee_id']
    username_args = request.args.get('username')
    if username_args and username_args != username:
        return jsonify({'message': 'Unauthorized!'}), 401

    employee = employee_db.get_employee(username_args or username)
    if employee:
        return jsonify(employee), 200
    else:
        return jsonify({'message': 'Employee not found!'}), 404
