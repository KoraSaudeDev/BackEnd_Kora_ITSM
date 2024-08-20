from flask import Blueprint, jsonify, request
from sqlalchemy import or_
from app.models.vw_itsm_grupos import VwItsmGrupos

access_blueprint = Blueprint('access', __name__)

@access_blueprint.route('/meus-grupos', methods=['GET'])
def get_meus_grupos():
    email = request.args.get('email')
    if not email:
        return jsonify({"error": "Email parameter is required"}), 400
    
    try:
        grupos = VwItsmGrupos.query.filter_by(email=email)

        result = [
            {
                "id": grupo.id,
                "id_grupo": grupo.id_grupo,
                "grupo": grupo.grupo,
                "id_papel": grupo.id_papel,
                "papel": grupo.papel
            }
            for grupo in grupos
        ]

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500