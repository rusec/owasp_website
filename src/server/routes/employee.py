from flask import Blueprint, jsonify, request
import jwt_utils
# import server.database.employee as employee_db

from lib.employee import Employee 

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

@employee_bp.route('/<int:employee_id>', methods=['GET'])
def get_employee_endpoint(employee_id):
    employee = Employee.get_employee_employee_id(employee_id)
    if employee:
        return jsonify(employee.to_json()), 200
    else:
        return jsonify({'message': 'Employee not found!'}), 404
