from flask import Flask, send_from_directory
import werkzeug
import routes.employee as employee_routes
import routes.users as user_routes
import routes.account as account_routes
import routes.chat as chat_routes
import os
from database.db import init_db

app = Flask(__name__, static_folder='static', static_url_path='/')



app.register_blueprint(employee_routes.employee_bp)
app.register_blueprint(user_routes.users_bp)
app.register_blueprint(account_routes.account_bp)
app.register_blueprint(chat_routes.chat_bp)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/login')
def login():
    return app.send_static_file('login.html')

@app.route('/about')
def about():
    return app.send_static_file('about.html')

@app.route('/dashboard')
def dashboard():
    return app.send_static_file('dashboard.html')

@app.route('/employee')
def employee():
    return app.send_static_file('employee.html')


@app.route('/employee/<path:path>')
def send_employee(path):
    static_url = os.path.join(app.static_folder, './employee')
    return send_from_directory(static_url, path + '.html')

@app.route('/forget/reset')
def forget_reset():
    static_url = os.path.join(app.static_folder, './forget')
    return send_from_directory(static_url, 'reset.html')

@app.route('/forget')
def forget():
    return app.send_static_file('forget.html')


@app.route('/health')
def health():
    return {"message": "healthy"}, 200


@app.errorhandler(500)
def handle_bad_request(e):
    return {"message": "Bad request", "error": e}, 500

if __name__ == '__main__':

    # Run the app on port 5000
    init_db()
    app.run("0.0.0.0", port=5000, debug=True, ssl_context='adhoc')
