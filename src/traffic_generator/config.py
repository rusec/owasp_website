import os

SERVER_HOST = os.getenv("SERVER_HOST", "127.0.0.1")
SERVER_PORT = os.getenv("SERVER_PORT", 5000)
HTTP_URL = f"https://{SERVER_HOST}:{SERVER_PORT}"
