import os 

# MySQL database configuration
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "root")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "app")

# JWT secret key for signing tokens
JWT_SECRET = os.getenv("JWT_SECRET", "By_the_eye_of_Agamotto")

# Vault server configuration
VAULT_SERVER_URL = os.getenv("VAULT_SERVER_URL", "http://localhost:5001")


ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")