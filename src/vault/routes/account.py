from Flask import Blueprint, request, jsonify
from vault.lib.account import Account
account_bp = Blueprint('account', __name__, url_prefix='/')


@account_bp.route('/transfer', methods=['POST'])
def transfer():
    data = request.get_json()
    account_from = data.get('account_from')
    account_to = data.get('account_to')
    amount = data.get('amount')

    if not account_from or not account_to or not amount:
        return jsonify({'message': 'Account from, account to and amount are required!'}), 400
    
    account_from = Account.get_account(account_from)
    account_to = Account.get_account(account_to)

    if not account_from or not account_to:
        return jsonify({'message': 'Account not found!'}), 404
    
    result = account_from.remove_balance(amount)
    if not result:
        return jsonify({'message': 'Transfer failed!'}), 500
    result = account_to.add_balance(amount)
    if not result:
        return jsonify({'message': 'Transfer failed!'}), 500


    return jsonify({'message': 'Transfer successful!'}), 200

@account_bp.route('/accounts/<str:account_number>', methods=['GET'])
def get_account(account_number):
    account_number = request.args.get('account_number')

    account = Account.get_account(account_number)
    if not account:
        return jsonify({'message': 'Account not found!'}), 404
    

@account_bp.route('/accounts/<str:account_number>', methods=['POST'])
def transfer_account_to_vault(account_number):
    data = request.get_json()
    account_number = data.get('account_number')

    if not account_number:
        return jsonify({'message': 'Account number is required!'}), 400
    
    account = Account.get_account(account_number)
    if account:
        return jsonify({'message': 'Account already Exists'}), 409
    
    result = Account.create_account(account_number)
    if not result:
        return jsonify({'message': 'Account creation failed!'}), 500
    
    return jsonify({'message': 'Account created successfully!'}), 201

@account_bp.route('/del_amount', methods=['POST'])
def del_amount():
    data = request.get_json()
    account_number = data.get('account_number')
    amount = data.get('amount')

    if not account_number or not amount:
        return jsonify({'message': 'Account number and amount are required!'}), 400
    
    account = Account.get_account(account_number)
    if not account:
        return jsonify({'message': 'Account not found!'}), 404
    
    result = account.remove_balance(amount)
    if not result:
        return jsonify({'message': 'Transfer failed!'}), 500

    return jsonify({'message': 'Transfer successful!'}), 200

@account_bp.route('/add_amount', methods=['POST'])
def add_amount():
    data = request.get_json()
    account_number = data.get('account_number')
    amount = data.get('amount')

    if not account_number or not amount:
        return jsonify({'message': 'Account number and amount are required!'}), 400
    
    account = Account.get_account(account_number)
    if not account:
        return jsonify({'message': 'Account not found!'}), 404
    
    result = account.add_balance(amount)
    if not result:
        return jsonify({'message': 'Transfer failed!'}), 500

    return jsonify({'message': 'Transfer successful!'}), 200
