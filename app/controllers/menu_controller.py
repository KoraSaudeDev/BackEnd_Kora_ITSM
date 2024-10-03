from flask import Blueprint, jsonify, request
from sqlalchemy import or_, and_, asc, desc, distinct
from app import db
from app.models.tb_suporte_menu import TbSuporteMenu
from app.utils.auth_utils import token_required

menu_blueprint = Blueprint('menu', __name__)

@menu_blueprint.route('/', methods=['GET'])
@token_required
def get_menus():
    try:
        menus = TbSuporteMenu.query.filter_by(active=True).order_by(TbSuporteMenu.ordem).all()
        menu_list = [
            {
                "id": menu.id, 
                "label": menu.label, 
                "route": menu.route, 
                "apiCounterConfig": menu.apiCounterConfig, 
                "icon": menu.icon, 
                "parent_id": menu.parent_id,
                "componentPath": menu.componentPath
            }
            for menu in menus
        ]
        return jsonify(menu_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500