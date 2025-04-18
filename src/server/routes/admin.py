from flask import Blueprint,jsonify, requests

admin_dp = Blueprint('admin',__name__, url_prefix="/api/admin")
