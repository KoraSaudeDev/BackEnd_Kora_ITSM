from flask import Blueprint, jsonify, request
from flask_mail import Message
from app import mail

email_blueprint = Blueprint('email', __name__)

@email_blueprint.route('/send', methods=['POST'])
def send_email_route():
    data = request.get_json()

    to = data.get('to')
    subject = data.get('subject')
    body = data.get('body')

    if not to or not subject or not body:
        return jsonify({"error": "Os campos 'to', 'subject' e 'body' são obrigatórios"}), 400

    cc = data.get('cc')
    bcc = data.get('bcc')

    try:
        send_email(to=to, subject=subject, body=body, cc=cc, bcc=bcc)
        return jsonify({"message": "Email enviado com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def send_email(to, subject, body, cc=None, bcc=None):
    msg = Message(
        subject=subject,
        recipients=[to],
        cc=cc if cc else [],
        bcc=bcc if bcc else [],
        html=body
    )
    mail.send(msg)