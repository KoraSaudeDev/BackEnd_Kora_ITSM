from flask import Flask, request
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
    
    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.before_request
    def log_request_info():
        x_user_email = request.headers.get('X-User-Email', 'N/A')
        referer = request.headers.get('Referer', 'N/A')
        print(f"{request.path} - X-User-Email: {x_user_email} - Referer: {referer}")

    from app.views.routes import main_blueprint
    app.register_blueprint(main_blueprint)

    return app