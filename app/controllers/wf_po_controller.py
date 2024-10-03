from flask import Blueprint, jsonify, request
from sqlalchemy import or_
from app import db
from app.models.vw_wf_po import VwWFPO
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
        query = VwWFPO.query.filter(VwWFPO.email == email)

        paginated_tickets = query.paginate(page=page, per_page=per_page, error_out=False)

        tickets_list = [
            {
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
        query = VwWFPO.query

        paginated_tickets = query.paginate(page=page, per_page=per_page, error_out=False)

        tickets_list = [
            {
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
