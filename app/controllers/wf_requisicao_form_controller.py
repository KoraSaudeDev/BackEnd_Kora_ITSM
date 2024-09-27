from flask import Blueprint, jsonify, request
from sqlalchemy import or_
from app import db
from app.models.vw_requisicao_compra_unidades import VwRequisicaoCompraUnidades

wf_requisicao_form_blueprint = Blueprint('wf_requisicao_form', __name__)

@wf_requisicao_form_blueprint.route('/hub', methods=['GET'])
def get_all_hubs():
    try:
        hubs = db.session.query(VwRequisicaoCompraUnidades.hub).distinct().all()
        result = [hub[0] for hub in hubs]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@wf_requisicao_form_blueprint.route('/unidade', methods=['GET'])
def get_unidade():
    hub = request.args.get('hub')

    if not hub:
        return jsonify({"error": "Hub parameter is required"}), 400
    
    try:
        unidades = db.session.query(
            VwRequisicaoCompraUnidades.unidade,
            VwRequisicaoCompraUnidades.nu_codigo_sap
        ).filter(
            VwRequisicaoCompraUnidades.hub == hub
        ).distinct().all()
        
        result = [{"unidade": unidade.unidade, "cod_sap": unidade.nu_codigo_sap} for unidade in unidades]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500