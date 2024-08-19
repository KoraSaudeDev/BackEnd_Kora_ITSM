from flask import Blueprint, jsonify, request
from sqlalchemy import or_
from app.models.tb_tickets import TbTickets

tickets_blueprint = Blueprint('tickets', __name__)

@tickets_blueprint.route('/meus-tickets', methods=['GET'])
def get_meus_tickets():
    email = request.args.get('email')
    if not email:
        return jsonify({"error": "Email parameter is required"}), 400

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    try:
        query = TbTickets.query.filter_by(email_solicitante=email)

        paginated_tickets = query.paginate(page=page, per_page=per_page, error_out=False)

        results = [
            {
                "id": ticket.id,
                "cod_fluxo": ticket.cod_fluxo,
                "abertura": ticket.abertura,
                "status": ticket.status,
                "sla_util": ticket.st_sla,
                "data_limite": ticket.data_limite,
                "grupo": ticket.grupo,
                "nome": ticket.nome,
                "area_negocio": ticket.area_negocio,
                "hub": ticket.hub,
                "unidade": ticket.unidade,
                "categoria": ticket.categoria,
                "subcategoria": ticket.subcategoria,
                "assunto": ticket.assunto 
            }
            for ticket in paginated_tickets.items
        ]

        return jsonify({
            "page": paginated_tickets.page,
            "pages": paginated_tickets.pages,
            "total_items": paginated_tickets.total,
            "items_per_page": paginated_tickets.per_page,
            "tickets": results
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@tickets_blueprint.route('/minha-equipe', methods=['GET'])
def get_minha_equipe():
    data = request.get_json()
    grupos = data.get('grupos', [])
    
    if not grupos:
        return jsonify({"error": "Grupos parameter is required"}), 400

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    try:
        like_conditions = [TbTickets.grupo.like(f"%{grupo}%") for grupo in grupos]
        
        query = TbTickets.query.filter(
            or_(*like_conditions),
            TbTickets.status.notin_(["Finalizado", "Cancelado"])
        )

        paginated_tickets = query.paginate(page=page, per_page=per_page, error_out=False)

        results = [
            {
                "id": ticket.id,
                "cod_fluxo": ticket.cod_fluxo,
                "abertura": ticket.abertura,
                "status": ticket.status,
                "sla_util": ticket.st_sla,
                "data_limite": ticket.data_limite,
                "grupo": ticket.grupo,
                "nome": ticket.nome,
                "area_negocio": ticket.area_negocio,
                "hub": ticket.hub,
                "unidade": ticket.unidade,
                "categoria": ticket.categoria,
                "subcategoria": ticket.subcategoria,
                "assunto": ticket.assunto,
            }
            for ticket in paginated_tickets.items
        ]

        return jsonify({
            "page": paginated_tickets.page,
            "pages": paginated_tickets.pages,
            "total_items": paginated_tickets.total,
            "items_per_page": paginated_tickets.per_page,
            "tickets": results
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@tickets_blueprint.route('/tickets-preview', methods=['GET'])
def get_tickets_preview():
    cod_fluxo = request.args.get('id')
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    try:
        query = TbTickets.query

        if cod_fluxo:
            query = query.filter(TbTickets.cod_fluxo.like(f'%{cod_fluxo}%'))
        
        paginated_tickets = query.paginate(page=page, per_page=per_page, error_out=False)

        results = [
            {
                "id": ticket.id,
                "cod_fluxo": ticket.cod_fluxo,
                "abertura": ticket.abertura,
                "status": ticket.status,
                "sla_util": ticket.st_sla,
                "data_limite": ticket.data_limite,
                "grupo": ticket.grupo,
                "nome": ticket.nome,
                "area_negocio": ticket.area_negocio,
                "hub": ticket.hub,
                "unidade": ticket.unidade,
                "categoria": ticket.categoria,
                "subcategoria": ticket.subcategoria,
                "assunto": ticket.assunto 
            }
            for ticket in paginated_tickets.items
        ]

        return jsonify({
            "page": paginated_tickets.page,
            "pages": paginated_tickets.pages,
            "total_items": paginated_tickets.total,
            "items_per_page": paginated_tickets.per_page,
            "tickets": results
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

