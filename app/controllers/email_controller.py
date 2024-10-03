from flask import Blueprint, jsonify, request, current_app
import threading
from app.utils.auth_utils import token_required
from app.utils.email_utils import send_email_async

email_blueprint = Blueprint('email', __name__)

@email_blueprint.route('/send', methods=['POST'])
@token_required
def send_email_route():
    data = request.get_json()

    to = data.get('to')
    subject = data.get('subject')
    body = data.get('body')

    if not to or not subject or not body:
        return jsonify({"error": "Os campos 'to', 'subject' e 'body' são obrigatórios"}), 400

    to_list = [email.strip() for email in to.split(';')]
    cc = data.get('cc')
    bcc = data.get('bcc')

    app_context = current_app._get_current_object()

    try:
        email_thread = threading.Thread(
            target=send_email_async,
            args=(app_context, to_list, subject, body),
            kwargs={'cc': cc, 'bcc': bcc}
        )
        email_thread.start()
        return jsonify({"message": "Email enviado com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500