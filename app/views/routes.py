from flask import Blueprint
from app.controllers.tickets_controller import tickets_blueprint
from app.controllers.access_controller import access_blueprint

main_blueprint = Blueprint('main', __name__)

main_blueprint.register_blueprint(tickets_blueprint, url_prefix='/tickets')
main_blueprint.register_blueprint(access_blueprint, url_prefix='/access')