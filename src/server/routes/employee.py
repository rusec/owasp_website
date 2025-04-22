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

    employee_json = employee.to_json()
    if not employee_json:
        return jsonify({'message': 'Employee not found!'}), 404

    employee_json.update({
        'employee_id': employee.employee_id,
        'role': 'employee',
    })

    # Generate JWT token
    token = jwt_utils.encode(employee_json)
    response =  jsonify({'token': token})
    response.set_cookie('Authorization', f'Bearer {token}')
    response.headers.add('Authorization', f'Bearer {token}')

    return response, 200

def check_employee_login():
    # Check if the user is logged in
    token = request.headers.get('Authorization')
    if not token:
        token = request.cookies.get("Authorization")

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




@employee_bp.route("/register", methods=["POST"])
def register_employee():
    data = request.get_json()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    avatar_url = data.get("avatar_url")

    if not username or not password:
        return jsonify({"message": "Username and password are required!"}), 400

    employee = Employee.register(username, password, first_name, last_name, email, avatar_url)
    if not employee:
        return jsonify({"message": "Employee already exists!"}), 409

    return jsonify({"message": "Employee registered successfully!"}), 201

@employee_bp.route("/info", methods=["GET"])
def get_employee_info():
    payload = check_employee_login()
    if type(payload) != dict:
        return payload
    employee_id = payload.get("employee_id")
    employee = Employee.get_employee_employee_id(employee_id)
    if employee:
        return jsonify(employee.to_json()), 200
    else:
        return jsonify({'message': 'Employee not found!'}), 404

@employee_bp.route("/bank", methods=["GET"])
def get_bank_status():
    employee = check_employee_login()
    if type(employee) != dict:
        return employee

    employee_id = employee.get("employee_id")
    if not employee_id:
        return jsonify({"message": "Employee ID not found!"}), 400

    employee = Employee.get_employee_employee_id(employee_id)
    if not employee:
        return jsonify({"message": "Employee not found!"}), 404

    bank_status = employee.get_back_status()
    if not bank_status:
        return jsonify({"message": "Bank status not found!"}), 404

    return jsonify(bank_status), 200


@employee_bp.route('/<int:employee_id>', methods=['GET'])
def get_employee_endpoint(employee_id):
    employee = Employee.get_employee_employee_id(employee_id)
    if employee:
        return jsonify(employee.to_json()), 200
    else:
        return jsonify({'message': 'Employee not found!'}), 404
