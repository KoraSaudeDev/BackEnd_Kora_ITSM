from flask import Blueprint, jsonify, request
from sqlalchemy import or_
from app import db
from app.models.vw_wf_po_unidades import VwWFPOUnidades
from app.models.tb_wf_po_fase import TbWFPOFase
from app.utils.auth_utils import token_required

wf_po_form_blueprint = Blueprint('wf_po_form', __name__)

@wf_po_form_blueprint.route('/hub', methods=['GET'])
@token_required
def get_all_hubs():
    try:
        hubs = db.session.query(VwWFPOUnidades.hub).distinct().all()
        result = [hub[0] for hub in hubs]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@wf_po_form_blueprint.route('/unidade', methods=['GET'])
@token_required
def get_unidade():
    hub = request.args.get('hub')

    if not hub:
        return jsonify({"error": "Hub parameter is required"}), 400
    
    try:
        unidades = db.session.query(
            VwWFPOUnidades.unidade,
            VwWFPOUnidades.nu_codigo_sap,
            VwWFPOUnidades.bloco_produto,
            VwWFPOUnidades.bloco_servico
        ).filter(
            VwWFPOUnidades.hub == hub
        ).distinct().all()
        
        result = [
            {
                "unidade": unidade.unidade,
                "cod_sap": unidade.nu_codigo_sap,
                "bloco_produto": unidade.bloco_produto,
                "bloco_servico": unidade.bloco_servico
            } for unidade in unidades
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@wf_po_form_blueprint.route('/fases', methods=['GET'])
@token_required
def buscar_fases():
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    bloco = request.args.get('bloco', '')
    valor = request.args.get('valor', '')
    fase = request.args.get('fase', '')

    if not bloco:
        return jsonify({"error": "Parâmetro 'bloco' é obrigatório"}), 400
    
    if not valor:
        return jsonify({"error": "Parâmetro 'valor' é obrigatório"}), 400
    
    if not is_number(valor):
        return jsonify({"error": "Parâmetro 'valor' deve conter apenas números"}), 400  

    tipo = None
    if "S/" in bloco: tipo = "Serviço"
    elif "P/" in bloco: tipo = "Produto"
    else: 
        return jsonify({"error": "Parâmetro 'bloco' precisa de um valor válido [P/1, P/2, P/3, P/CORP, S/1, S/CORP]"}), 400
    
    try:
        query = db.session.query(
            TbWFPOFase.n_ordem,
            TbWFPOFase.id_grupo,
            TbWFPOFase.n_alcada_limit
        )
        
        if not fase:
            # Filtrando sem o parâmetro de 'fase'
            query = query.filter(
                (TbWFPOFase.n_bloco == bloco) & 
                ((TbWFPOFase.n_alcada_limit <= valor) |
                 (TbWFPOFase.n_alcada_limit == db.session.query(
                     db.func.min(TbWFPOFase.n_alcada_limit)
                 ).filter(
                     TbWFPOFase.n_bloco == bloco,
                     TbWFPOFase.n_alcada_limit >= valor
                 ).scalar_subquery()))
            ).union_all(
                db.session.query(
                    TbWFPOFase.n_ordem,
                    TbWFPOFase.id_grupo,
                    TbWFPOFase.n_alcada_limit
                ).filter(
                    TbWFPOFase.n_bloco.is_(None),
                    TbWFPOFase.n_ordem > 14,
                    TbWFPOFase.n_alcada_limit.is_(None)
                )
            ).union_all(
                db.session.query(
                    TbWFPOFase.n_ordem,
                    TbWFPOFase.id_grupo,
                    TbWFPOFase.n_alcada_limit
                ).filter(
                    TbWFPOFase.n_bloco.is_(None),
                    TbWFPOFase.n_alcada_limit.isnot(None),
                    TbWFPOFase.ds_tipo_compra == tipo,
                    ((TbWFPOFase.n_alcada_limit <= valor) |
                     (TbWFPOFase.n_alcada_limit == db.session.query(
                         db.func.min(TbWFPOFase.n_alcada_limit)
                     ).filter(
                         TbWFPOFase.n_bloco.is_(None),
                         TbWFPOFase.n_alcada_limit.isnot(None),
                         TbWFPOFase.ds_tipo_compra == tipo,
                         TbWFPOFase.n_alcada_limit >= valor
                     ).scalar_subquery()))
                )
            )
        else:
            if not is_number(fase):
                return jsonify({"error": "Parâmetro 'fase' deve conter apenas números"}), 400
            
            # Filtrando com o parâmetro 'fase'
            query = query.filter(
                (TbWFPOFase.n_bloco == bloco) & 
                ((TbWFPOFase.n_alcada_limit <= valor) |
                 (TbWFPOFase.n_alcada_limit == db.session.query(
                     db.func.min(TbWFPOFase.n_alcada_limit)
                 ).filter(
                     TbWFPOFase.n_bloco == bloco,
                     TbWFPOFase.n_alcada_limit >= valor
                 ).scalar_subquery())) & 
                (TbWFPOFase.n_ordem > fase)
            ).union_all(
                db.session.query(
                    TbWFPOFase.n_ordem,
                    TbWFPOFase.id_grupo,
                    TbWFPOFase.n_alcada_limit
                ).filter(
                    TbWFPOFase.n_bloco.is_(None),
                    TbWFPOFase.n_ordem > fase,
                    TbWFPOFase.n_alcada_limit.is_(None)
                )
            ).union_all(
                db.session.query(
                    TbWFPOFase.n_ordem,
                    TbWFPOFase.id_grupo,
                    TbWFPOFase.n_alcada_limit
                ).filter(
                    TbWFPOFase.n_bloco.is_(None),
                    TbWFPOFase.n_alcada_limit.isnot(None),
                    TbWFPOFase.ds_tipo_compra == tipo,
                    ((TbWFPOFase.n_alcada_limit <= valor) |
                     (TbWFPOFase.n_alcada_limit == db.session.query(
                         db.func.min(TbWFPOFase.n_alcada_limit)
                     ).filter(
                         TbWFPOFase.n_bloco.is_(None),
                         TbWFPOFase.n_alcada_limit.isnot(None),
                         TbWFPOFase.ds_tipo_compra == tipo,
                         TbWFPOFase.n_alcada_limit >= valor
                     ).scalar_subquery())) &
                    (TbWFPOFase.n_ordem > fase)
                )
            )

        fases = query.order_by(TbWFPOFase.n_ordem.asc()).all()

        fases_list = [{"id_fase": row[0], "id_grupo": row[1], "valor_limite_alcada": row[2]} for row in fases]

        return jsonify(fases_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500