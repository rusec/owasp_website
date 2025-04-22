from flask import Blueprint, jsonify, request
from routes.users import check_login
import database.accounts as account_db
import database.users as user_db
from lib.user import User


account_bp = Blueprint('account', __name__, url_prefix='/api/account')

@account_bp.route('/transfer', methods=['POST'])
def transfer():
    user = check_login()
    if type(user) != dict:
        return user

    data = request.get_json()
    account_to = data.get('account_to')
    amount = data.get('amount')

    if not account_to or not amount:
        return jsonify({'message': 'account to and amount are required!'}), 400

    if type(amount) != float:
        return jsonify({'message': 'amount must be a float! '}), 400

    if amount <= 0:
        return jsonify({'message': 'Amount must be greater than 0!'}), 400

    user_id = user.get('user_id')
    if not user_id:
        return jsonify({'message': 'User ID not found!'}), 400

    user = User.get_user_by_id(user_id)
    if not user:
        return jsonify({'message': 'User not found!'}), 404

    account = user.get_account()
    if not account:
        return jsonify({'message': 'Account not found!'}), 404

    account_to = int(account_to)


    if account.account_number == account_to:
        return jsonify({'message': 'Account from and account to must be different!'}), 400

    result = account.transfer_funds(account_to, amount)
    if not result:
        return jsonify({'message': 'Transfer failed!'}), 500

    return jsonify({'message': 'Transfer successful!'}), 200


@account_bp.route('/transactions', methods=['GET'])
def get_transactions():
    user_payload = check_login()
    if type(user_payload) != dict:
        return user_payload

    user_id = user_payload.get('user_id')
    if not user_id:
        return jsonify({'message': 'User ID not found!'}), 400

    user = User.get_user_by_id(user_id)
    if not user:
        return jsonify({'message': 'User not found!'}), 404

    account = user.get_account()
    if not account:
        return jsonify({'message': 'Account not found!'}), 404

    transactions = account.get_transactions()
    if not transactions:
        return jsonify({'message': 'No transactions found!'}), 404

    return jsonify(transactions), 200


@account_bp.route('/<int:account_number>', methods=['GET'])
def get_account(account_number):
    user_payload = check_login()
    if type(user_payload) != dict:
        return user_payload
    user_id = user_payload.get('user_id')
    if not user_id:
        return jsonify({'message': 'User ID not found!'}), 400


    user = user_db.get_user_by_id(user_id)

    if not user:
        return jsonify({'message': 'User not found!'}), 404

    # Still uses older get_account function without user id check
    account = account_db.get_account(user['account_number'], user_id)
    # (SSRF) because the get account function does not check if the user id matches the account for vault accounts
    if account_number and account_number != user['account_number']:
        account = account_db.get_account(account_number,user_id)

    if not account:
        return jsonify({'message': 'Account not found!'}), 404

    return jsonify(account), 200
