from flask import Blueprint, jsonify, request
from sqlalchemy import or_
from app.models.vw_itsm_filas_usuarios import VwItsmFilasUsuarios
from app.models.vw_itsm_filas_gestores import VwItsmFilasGestores
from app.models.vw_wf_po_usuarios import VwWFPOUsuarios
from app.models.tb_users_new import TbUsersNew
from app.utils.auth_utils import token_required

access_blueprint = Blueprint('access', __name__)

@access_blueprint.route('/minhas-filas', methods=['GET'])
@token_required
def get_minhas_filas():
    email = request.args.get('email')
    if not email:
        return jsonify({"error": "Email parameter is required"}), 400

    try:
        user = TbUsersNew.query.filter_by(ds_email=email).first()
        if not user:
            return jsonify({})

        result = {
            "id_user": user.id,
            "filas_id": [],
            "filas": [],
            "wf_po_grupos": [],
            "wf_po_grupos_id": []
        }

        if user.bl_gestao == 1:
            result["gestor"] = {}
            gestor_filas = VwItsmFilasGestores.query.filter_by(id_user=user.id).all()
            for fila in gestor_filas:
                result["gestor"][fila.id_fila] = {
                    "id_fila": fila.id_fila,
                    "fila": fila.fila,
                    "usuarios": []
                }
                
                usuarios_fila = VwItsmFilasUsuarios.query.filter_by(id_fila=fila.id_fila).all()
                result["gestor"][fila.id_fila]["usuarios"] = [usuario.id_user for usuario in usuarios_fila]

            result["filas_id"] = [fila.id_fila for fila in gestor_filas]
            result["filas"] = [fila.fila for fila in gestor_filas]
        else:
            filas = VwItsmFilasUsuarios.query.filter_by(id_user=user.id).all()
            result["filas_id"] = [fila.id_fila for fila in filas]
            result["filas"] = [fila.fila for fila in filas]
            
        grupos = VwWFPOUsuarios.query.filter_by(id_user=user.id).all()
        result["wf_po_grupos"] = [grupo.grupo for grupo in grupos]
        result["wf_po_grupos_id"] = [grupo.id_grupo for grupo in grupos]

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500