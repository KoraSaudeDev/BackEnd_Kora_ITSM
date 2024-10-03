from flask_mail import Message
from app import mail

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