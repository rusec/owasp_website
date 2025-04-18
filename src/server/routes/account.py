from flask import Blueprint, jsonify, request
from users import check_login
import server.database.accounts as account_db
import server.database.users as user_db
from server.lib.account import Account
from server.lib.user import User, get_user_by_id
account_bp = Blueprint('account', __name__, url_prefix='/api/account')



@account_bp.route('/transfer', methods=['POST'])
def transfer():
    user = check_login()
    if type(user) != dict:
        return user

    data = request.get_json()

    # account_from = data.get('account_from')
    account_to = data.get('account_to')
    amount = data.get('amount')

    if  not account_to or not amount:
        return jsonify({'message': 'Account from, account to and amount are required!'}), 400

    if  type(account_to) != str or type(amount) != float:
        return jsonify({'message': 'Account from and account to must be strings and amount must be a float!'}), 400

    if amount <= 0:
        return jsonify({'message': 'Amount must be greater than 0!'}), 400


    user_id = user['user_id']

    user = get_user_by_id(user_id)
    if not user:
        return jsonify({'message': 'User not found!'}), 404

    account = user.get_account()
    if not account:
        return jsonify({'message': 'Account not found!'}), 404

    if account.account_number == account_to:
        return jsonify({'message': 'Account from and account to must be different!'}), 400

    result = account.transfer_funds(account_to['account_number'], amount)
    if not result:
        return jsonify({'message': 'Transfer failed!'}), 500

    return jsonify({'message': 'Transfer successful!'}), 200

@account_bp.route('/', methods=['GET'])
@account_bp.route('/<string:account_number>', methods=['GET'])
def get_account():
    user_payload = check_login()
    if type(user_payload) != dict:
        return user_payload
    user_id = user_payload['user_id']
    account_number_args = request.args.get('account_number')

    user = user_db.get_user_by_id(user_id)

    if not user:
        return jsonify({'message': 'User not found!'}), 404

    # Still uses older get_account function without user id check
    account = account_db.get_account(user['account_number'], user_id)
    # (SSRF) because the get account function does not check if the user id matches the account for vault accounts
    if account_number_args and account_number_args != user['account_number']:
        account = account_db.get_account(account_number_args,user_id)

    if not account:
        return jsonify({'message': 'Account not found!'}), 404

    return jsonify(account), 200
