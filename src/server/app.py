from flask import Flask
import routes.employee as employee_routes
import routes.users as user_routes
app = Flask(__name__, static_folder='../../static', static_url_path='/')



app.register_blueprint(employee_routes.employee_bp)
app.register_blueprint(user_routes.users_bp)

@app.route('/api/health')
def health():
    return {"message": "healthy"}


if __name__ == '__main__':
    # Run the app on port 5000
    app.run("0.0.0.0", port=5000, debug=True)
