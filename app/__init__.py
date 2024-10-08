from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_cors import CORS

db = SQLAlchemy()
mail = Mail()

ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://helper.korasaude.com.br",
    "https://qashelper.korasaude.com.br"
]

ALLOWED_VPN_IPS = ["192.168.80.0/24", "10.188.233.36", "127.0.0.1"]

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    mail.init_app(app)
    
    CORS(app, resources={r"/*": {"origins": ALLOWED_ORIGINS}})

    @app.before_request
    def log_request_info():
        x_user_email = request.headers.get('X-User-Email', 'N/A')
        referer = request.headers.get('Referer', 'N/A')
        print(f"{request.path} - X-User-Email: {x_user_email} - Referer: {referer}")

        origin = request.headers.get('Origin')
        if origin not in ALLOWED_ORIGINS:
            client_ip = request.remote_addr

            if not any(ip_in_subnet(client_ip, subnet) for subnet in ALLOWED_VPN_IPS):
                abort(403)

    from app.views.routes import main_blueprint
    app.register_blueprint(main_blueprint)

    return app

def ip_in_subnet(ip, subnet):
    from ipaddress import ip_address, ip_network
    return ip_address(ip) in ip_network(subnet)