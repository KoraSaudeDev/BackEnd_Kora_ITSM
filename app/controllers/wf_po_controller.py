from flask import Blueprint, jsonify, request
from sqlalchemy import or_
from app import db
from app.models.vw_wf_po import VwWFPO
from app.models.vw_wf_po_materiais import VwWFPOMateriais
from app.models.vw_wf_po_aprovacoes import VwWFPOAprovacoes
from app.models.vw_wf_po_task import VwWFPOTasks
from app.models.vw_wf_po_bionexo import VwWFPOBionexo
from app.utils.auth_utils import token_required

wf_po_blueprint = Blueprint('wf_po', __name__)

@wf_po_blueprint.route('/meus-tickets', methods=['GET'])
@token_required
def get_meus_tickets():
    email = request.args.get('email')
    if not email:
        return jsonify({"error": "Email parameter is required"}), 400

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    try:
        query = VwWFPO.query.filter(VwWFPO.email == email).order_by(VwWFPO.id.desc())

        paginated_tickets = query.paginate(page=page, per_page=per_page, error_out=False)

        tickets_list = [
            {
                "id": ticket.id,
                "dt_abertura": ticket.dt_abertura,
                "executor": ticket.executor,
                "email": ticket.email,
                "nome": ticket.nome,
                "hub": ticket.hub,
                "unidade": ticket.unidade,
                "centro_custo": ticket.centro_custo,
                "numero_bloco": ticket.numero_bloco,
                "fase": ticket.fase,
                "tipo_solicitacao": ticket.tipo_solicitacao,
                "grupo_material": ticket.grupo_material
            }
            for ticket in paginated_tickets.items
        ]

        return jsonify({
            "page": paginated_tickets.page,
            "pages": paginated_tickets.pages,
            "total_items": paginated_tickets.total,
            "items_per_page": paginated_tickets.per_page,
            "tickets": tickets_list
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@wf_po_blueprint.route('/acompanhar', methods=['GET'])
@token_required
def get_all():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    try:
        query = VwWFPO.query.order_by(VwWFPO.id.desc())

        paginated_tickets = query.paginate(page=page, per_page=per_page, error_out=False)

        tickets_list = [
            {
                "id": ticket.id,
                "dt_abertura": ticket.dt_abertura,
                "executor": ticket.executor,
                "email": ticket.email,
                "nome": ticket.nome,
                "hub": ticket.hub,
                "unidade": ticket.unidade,
                "centro_custo": ticket.centro_custo,
                "numero_bloco": ticket.numero_bloco,
                "fase": ticket.fase,
                "tipo_solicitacao": ticket.tipo_solicitacao,
                "grupo_material": ticket.grupo_material
            }
            for ticket in paginated_tickets.items
        ]

        return jsonify({
            "page": paginated_tickets.page,
            "pages": paginated_tickets.pages,
            "total_items": paginated_tickets.total,
            "items_per_page": paginated_tickets.per_page,
            "tickets": tickets_list
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@wf_po_blueprint.route('/aprovacoes', methods=['GET'])
@token_required
def get_aprovacoes():
    grupos = request.args.get('grupos')
    if not grupos:
        return jsonify({"error": "grupos parameter is required"}), 400
    
    email = request.args.get('email')
    if not email:
        return jsonify({"error": "email parameter is required"}), 400
    
    grupo_ids = [int(g.strip()) for g in grupos.split(',')]
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    try:
        query = VwWFPO.query.filter(VwWFPO.id_executor.in_(grupo_ids))
        
        query = query.union(
            VwWFPO.query.filter(VwWFPO.id_executor == 1, VwWFPO.email == email)
        )
        
        query = query.order_by(VwWFPO.id.desc())

        paginated_tickets = query.paginate(page=page, per_page=per_page, error_out=False)

        tickets_list = [
            {
                "id": ticket.id,
                "dt_abertura": ticket.dt_abertura,
                "executor": ticket.executor,
                "email": ticket.email,
                "nome": ticket.nome,
                "hub": ticket.hub,
                "unidade": ticket.unidade,
                "centro_custo": ticket.centro_custo,
                "numero_bloco": ticket.numero_bloco,
                "fase": ticket.fase,
                "tipo_solicitacao": ticket.tipo_solicitacao,
                "grupo_material": ticket.grupo_material
            }
            for ticket in paginated_tickets.items
        ]

        return jsonify({
            "page": paginated_tickets.page,
            "pages": paginated_tickets.pages,
            "total_items": paginated_tickets.total,
            "items_per_page": paginated_tickets.per_page,
            "tickets": tickets_list
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@wf_po_blueprint.route('/wf-po', methods=['GET'])
@token_required
def get_requisicao():
    id = request.args.get('id')
    if not id:
        return jsonify({"error": "id parameter is required"}), 400

    try:
        ticket = VwWFPO.query.filter_by(id=id).first()
        
        if ticket:
            result = {
                "id": ticket.id,
                "dt_abertura": ticket.dt_abertura,
                "id_executor": ticket.id_executor,
                "executor": ticket.executor,
                "email": ticket.email,
                "nome": ticket.nome,
                "area": ticket.area,
                "hub": ticket.hub,
                "unidade": ticket.unidade,
                "centro_custo": ticket.centro_custo,
                "numero_bloco": ticket.numero_bloco,
                "id_fase": ticket.id_fase,
                "fase": ticket.fase,
                "tipo_solicitacao": ticket.tipo_solicitacao,
                "grupo_material": ticket.grupo_material,
                "total_materiais": str(ticket.total_materiais),
                "descricao": ticket.descricao,
                "observacoes": ticket.observacoes,
                "motivo_solicitacao": ticket.motivo_solicitacao,
                "id_bionexo": ticket.id_bionexo,
                "crtl_bionexo": ticket.crtl_bionexo,
                "id_sap": ticket.id_sap,
                "dt_remessa": ticket.dt_remessa,
                "cod_fornecedor": ticket.cod_fornecedor,
                "fornecedor": ticket.fornecedor,
                "dt_inicio_serv": ticket.dt_inicio_serv,
                "dt_fim_serv": ticket.dt_fim_serv
            }

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@wf_po_blueprint.route('/wf-po-materiais', methods=['GET'])
@token_required
def get_materiais():
    referencia_id = request.args.get('referencia_id')
    if not referencia_id:
        return jsonify({"error": "referencia_id parameter is required"}), 400

    try:
        materiais = VwWFPOMateriais.query.filter_by(referencia_id=referencia_id).all()
        
        if materiais:
            result = [{
                "id": item.id,
                "referencia_id": item.referencia_id,
                "codigo": item.codigo,
                "grupo": item.grupo,
                "material": item.material,
                "qtd": item.qtd,
                "preco": str(item.preco),
                "total": str(item.total),
                "id_status": item.id_status,
                "status": item.status,
                "motivo_reprova": item.motivo_reprova,
                "cnpj_fornecedor": item.cnpj_fornecedor
            } for item in materiais]

            return jsonify(result), 200
        return jsonify({"error": "No records found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@wf_po_blueprint.route('/wf-po-aprovacoes', methods=['GET'])
@token_required
def get_hist_aprovacoes():
    referencia_id = request.args.get('referencia_id')
    if not referencia_id:
        return jsonify({"error": "referencia_id parameter is required"}), 400

    try:
        aprovacoes = VwWFPOAprovacoes.query.filter_by(referencia_id=referencia_id).all()
        
        if aprovacoes:
            result = [{
                "id": item.id,
                "referencia_id": item.referencia_id,
                "codigo": item.codigo,
                "grupo": item.grupo,
                "material": item.material,
                "qtd": item.qtd,
                "preco": str(item.preco),
                "total": str(item.total),
                "id_status": item.id_status,
                "status": item.status,
                "id_executor": item.id_executor,
                "executor": item.executor,
                "aprovador": item.aprovador,
                "motivo_reprova": item.motivo_reprova
            } for item in aprovacoes]

            return jsonify(result), 200
        return jsonify({"error": "No records found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@wf_po_blueprint.route('/wf-po-tasks', methods=['GET'])
@token_required
def get_tasks():
    referencia_id = request.args.get('referencia_id')
    if not referencia_id:
        return jsonify({"error": "referencia_id parameter is required"}), 400

    try:
        tasks = VwWFPOTasks.query.filter_by(referencia_id=referencia_id).all()
        
        if tasks:
            result = [{
                "id": item.id,
                "referencia_id": item.referencia_id,
                "id_fase": item.id_fase,
                "fase": item.fase,
                "id_executor": item.id_executor,
                "executor": item.executor,
                "nome_executor": item.nome_executor,
                "numero_bloco": item.numero_bloco,
                "inicio": item.inicio,
                "fim": item.fim,
                "motivo_reprova": item.motivo_reprova
            } for item in tasks]

            return jsonify(result), 200
        return jsonify({"error": "No records found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@wf_po_blueprint.route('/wf-po-bionexo', methods=['GET'])
@token_required
def get_bionexo():
    referencia_id = request.args.get('referencia_id')
    if not referencia_id:
        return jsonify({"error": "referencia_id parameter is required"}), 400

    try:
        bionexo = VwWFPOBionexo.query.filter_by(referencia_id=referencia_id).all()
        
        if bionexo:
            result = [{
                "id": item.id,
                "referencia_id": item.referencia_id,
                "cnpj": item.cnpj,
                "razao_social": item.razao_social,
                "faturamento_min": str(item.faturamento_min),
                "prazo_entrega": item.prazo_entrega,
                "validade_proposta": item.validade_proposta,
                "id_forma_pag": item.id_forma_pag,
                "frete": item.frete,
                "observacao": item.observacao,
                "cod_produto": item.cod_produto,
                "quantidade": item.quantidade,
                "fabricante": item.fabricante,
                "embalagem": item.embalagem,
                "preco_unitario": str(item.preco_unitario),
                "preco_total": str(item.preco_total),
                "comentario": item.comentario,
                "inserido_em": item.inserido_em
            } for item in bionexo]

            return jsonify(result), 200
        return jsonify({"error": "No records found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
