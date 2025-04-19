from flask import Flask, jsonify, request
from vault.routes.account import account_bp
app = Flask(__name__)


app.register_blueprint(account_bp, url_prefix='/')


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200


if __name__ == '__main__':
    app.run("0.0.0.0", port=5001, debug=True)
