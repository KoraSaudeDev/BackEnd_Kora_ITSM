from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_cors import CORS

db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    mail.init_app(app)
    
    CORS(app, resources={r"/*": {"origins": [
        "https://helper.korasaude.com.br",
        "https://qashelper.korasaude.com.br",
        "http://localhost:3000"
    ]}})

    @app.before_request
    def log_request_info():
        x_user_email = request.headers.get('X-User-Email', 'N/A')
        referer = request.headers.get('Referer', 'N/A')
        print(f"{request.path} - X-User-Email: {x_user_email} - Referer: {referer}")

        allowed_origins = [
            "https://helper.korasaude.com.br",
            "https://qashelper.korasaude.com.br",
            "http://localhost:3000"
        ]

        origin = request.headers.get('Origin')
        user_agent = request.headers.get('User-Agent', '').lower()
        
        allowed_ip = '10.188.233.36'
        
        if request.headers.getlist("X-Forwarded-For"):
            request_ip = request.headers.getlist("X-Forwarded-For")[0]
        else:
            request_ip = request.remote_addr
        
        print("REQUEST IP",request_ip, request.headers)

        disallowed_agents = ['postman', 'insomnia', 'soapui']

        if origin not in allowed_origins and request_ip != allowed_ip:
            return jsonify({'error': 'Origin or IP not allowed'}), 403

        if request_ip != allowed_ip and any(agent in user_agent for agent in disallowed_agents):
            return jsonify({'error': 'Requests from this tool are not allowed from this IP'}), 403

    from app.views.routes import main_blueprint
    app.register_blueprint(main_blueprint)

    return app