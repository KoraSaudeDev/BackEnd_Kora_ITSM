from flask import Blueprint
from app.controllers.auth_controller import auth_blueprint
from app.controllers.tickets_controller import tickets_blueprint
from app.controllers.tickets_form_controller import tickets_form_blueprint
from app.controllers.tickets_update_controller import tickets_update_blueprint
from app.controllers.access_controller import access_blueprint
from app.controllers.tickets_files_controller import tickets_files_blueprint
from app.controllers.email_controller import email_blueprint
from app.controllers.chat_controller import chat_blueprint
from app.controllers.menu_controller import menu_blueprint
from app.controllers.sap_controller import sap_blueprint
from app.controllers.wf_po_controller import wf_po_blueprint
from app.controllers.wf_po_form_controller import wf_po_form_blueprint
from app.controllers.wf_po_update_controller import wf_po_update_blueprint

main_blueprint = Blueprint('main', __name__)

main_blueprint.register_blueprint(auth_blueprint)
main_blueprint.register_blueprint(tickets_blueprint, url_prefix='/tickets')
main_blueprint.register_blueprint(tickets_form_blueprint, url_prefix='/tickets/form')
main_blueprint.register_blueprint(tickets_update_blueprint, url_prefix='/tickets/update')
main_blueprint.register_blueprint(access_blueprint, url_prefix='/access')
main_blueprint.register_blueprint(tickets_files_blueprint, url_prefix='/tickets/file')
main_blueprint.register_blueprint(email_blueprint, url_prefix='/email')
main_blueprint.register_blueprint(chat_blueprint, url_prefix='/chat')
main_blueprint.register_blueprint(menu_blueprint, url_prefix='/menu')
main_blueprint.register_blueprint(sap_blueprint, url_prefix='/sap')
main_blueprint.register_blueprint(wf_po_blueprint, url_prefix='/wf-po')
main_blueprint.register_blueprint(wf_po_form_blueprint, url_prefix='/wf-po/form')
main_blueprint.register_blueprint(wf_po_update_blueprint, url_prefix='/wf-po/update')