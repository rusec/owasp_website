from flask import Blueprint, jsonify, request
import jwt_utils
import server.database.users as user_db 

users_bp = Blueprint('users', __name__, url_prefix='/api/user')


@users_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')


    if not username or not password and type(username) != str and type(password) != str:
        return jsonify({'message': 'Username and password are required!'}), 400
    
    
    if user_db.login(username, password) == False:
        return jsonify({'message': 'Invalid credentials!'}), 401
    # Generate JWT token
    token = jwt_utils.encode({'username': username })


    request.headers['Authorization'] = f'Bearer {token}'
    request.cookies['Authorization'] = f'Bearer {token}'


    return jsonify({'token': token}), 200

def check_login():
    # Check if the user is logged in
    token = request.headers.get('Authorization')
    
    if not token:
        return jsonify({'message': 'Unauthorized!'}), 401
    try:
        payload = jwt_utils.decode(token)

        return payload
    except jwt_utils.ExpiredSignatureError:
        return jsonify({'message': 'Token expired!'}), 401
    except jwt_utils.InvalidTokenError:
        return jsonify({'message': 'Invalid token!'}), 401
    

@users_bp.route('/', methods=['GET'])
@users_bp.route('/<str:username>', methods=['GET'])
def get_user():
    payload = check_login()
    if type(payload) != dict:
        return payload
    
    username = payload['username']
    username_args = request.view_args.get('username')
    if username_args and username_args != username:
            return jsonify({'message': 'Unauthorized!'}), 401
    
    user = user_db.get_user(username_args or username)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({'message': 'User not found!'}), 404
    
