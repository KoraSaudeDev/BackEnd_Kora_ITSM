from flask import Blueprint
from app.controllers.tickets_controller import tickets_blueprint
from app.controllers.tickets_form_controller import tickets_form_blueprint
from app.controllers.tickets_update_controller import tickets_update_blueprint
from app.controllers.access_controller import access_blueprint

main_blueprint = Blueprint('main', __name__)

main_blueprint.register_blueprint(tickets_blueprint, url_prefix='/tickets')
main_blueprint.register_blueprint(tickets_form_blueprint, url_prefix='/tickets/form')
main_blueprint.register_blueprint(tickets_update_blueprint, url_prefix='/tickets/update')
main_blueprint.register_blueprint(access_blueprint, url_prefix='/access')