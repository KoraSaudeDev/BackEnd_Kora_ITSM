from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    mail.init_app(app)

    from app.views.routes import main_blueprint
    app.register_blueprint(main_blueprint)

    return app