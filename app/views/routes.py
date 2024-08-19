from flask import Blueprint
from app.controllers.tickets_controller import tickets_blueprint

main_blueprint = Blueprint('main', __name__)

main_blueprint.register_blueprint(tickets_blueprint)
