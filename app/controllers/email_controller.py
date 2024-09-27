from flask import Blueprint, jsonify, request, current_app
from flask_mail import Message
from app import mail
import threading

email_blueprint = Blueprint('email', __name__)

@email_blueprint.route('/send', methods=['POST'])
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

def send_email_async(app, to, subject, body, cc=None, bcc=None):
    with app.app_context():
        msg = Message(
            subject=subject,
            recipients=to,
            cc=cc if cc else [],
            bcc=bcc if bcc else [],
            html=body
        )
        mail.send(msg)