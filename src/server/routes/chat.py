from flask import Blueprint, jsonify, request,stream_with_context, Response
from lib.chat import chatroom
from routes.employee import check_employee_login
from lib.employee import get_employee_by_id

chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')


@chat_bp.route('/', methods=['GET'])
def chat_stream():
    return Response(stream_with_context(chatroom.listen()), content_type='text/event-stream')

@chat_bp.route('/messages', methods=['GET'])
def get_messages():
    employee = check_employee_login()
    if type(employee) != dict:
        return employee

    messages = chatroom.get_history()
    if not messages:
        return jsonify({'message': 'No messages found'}), 404

    return jsonify(messages), 200

@chat_bp.route('/publish', methods=['POST'])
def publish_message():
    employee = check_employee_login()
    if type(employee) != dict:
        return employee
    data = request.get_json()
    message = data.get('message')

    if not message:
        return jsonify({'error': 'Message is required'}), 400

    if type(message) != str:
        return jsonify({'error': 'Message must be a string'}), 400

    employee = get_employee_by_id(employee['employee_id'])
    if not employee:
        return jsonify({'error': 'Employee not found'}), 404

    employee.chat(message)

    return jsonify({'status': 'Message published successfully'}), 200
