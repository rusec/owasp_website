from flask import Flask
import werkzeug
import routes.employee as employee_routes
import routes.users as user_routes
import routes.account as account_routes
import routes.chat as chat_routes
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

@app.route('/forgot')
def forgot():
    return app.send_static_file('forgot.html')

@app.route('/health')
def health():
    return {"message": "healthy"}, 200


@app.errorhandler(500)
def handle_bad_request(e):
    return {"message": "Bad request", "error": e}, 500

if __name__ == '__main__':

    # Run the app on port 5000
    init_db()
    app.run("0.0.0.0", port=5000, debug=True)
