from flask import Blueprint, jsonify, request
from sqlalchemy import or_
from app.models.vw_itsm_filas_usuarios import VwItsmFilasUsuarios
from app.models.tb_users_new import TbUsersNew

access_blueprint = Blueprint('access', __name__)

@access_blueprint.route('/minhas-filas', methods=['GET'])
def get_minhas_filas():
    email = request.args.get('email')
    if not email:
        return jsonify({"error": "Email parameter is required"}), 400

    try:
        user = TbUsersNew.query.filter_by(ds_email=email).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        filas = VwItsmFilasUsuarios.query.filter_by(id_user=user.id).all()

        result = {
            "id_user": user.id,
            "filas_id": [fila.id_fila for fila in filas],
            "filas": [fila.fila for fila in filas]
        }

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500