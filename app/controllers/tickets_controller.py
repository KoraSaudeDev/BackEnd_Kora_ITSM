from flask import Blueprint, jsonify, request
from sqlalchemy import or_
from app.models.tb_tickets import TbTickets
from app.models.tb_tickets_tasks import TbTicketsTasks

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

@tickets_blueprint.route('/ticket', methods=['GET'])
def get_ticket():
    cod_fluxo = request.args.get('cod_fluxo')
    if not cod_fluxo:
        return jsonify({"error": "Cod_fluxo parameter is required"}), 400

    try:
        tickets = TbTickets.query.filter_by(cod_fluxo=cod_fluxo).all()

        results = [
            {
                "id": ticket.id,
                "cod_fluxo": ticket.cod_fluxo,
                "abertura": ticket.abertura,
                "data_fim": ticket.data_fim,
                "finalizado_por": ticket.finalizado_por,
                "cancelado_por": ticket.cancelado_por,
                "status": ticket.status,
                "data_limite": ticket.data_limite,
                "st_sla": ticket.st_sla,
                "st_sla_corrido": ticket.st_sla_corrido,
                "ds_nivel": ticket.ds_nivel,
                "grupo": ticket.grupo,
                "nome": ticket.nome,
                "matricula": ticket.matricula,
                "telefone": ticket.telefone,
                "email_solicitante": ticket.email_solicitante,
                "cargo_solic": ticket.cargo_solic,
                "area_negocio": ticket.area_negocio,
                "departamento": ticket.departamento,
                "hub": ticket.hub,
                "unidade": ticket.unidade,
                "categoria": ticket.categoria,
                "subcategoria": ticket.subcategoria,
                "assunto": ticket.assunto,
                "descricao": ticket.descricao,
                "novo_usuario": ticket.novo_usuario,
                "primeiro_nome_user": ticket.primeiro_nome_user,
                "sobrenome_user": ticket.sobrenome_user,
                "email_user": ticket.email_user,
                "usuario_mv": ticket.usuario_mv,
                "dt_nascimento": ticket.dt_nascimento,
                "cpf": ticket.cpf,
                "matricula_senior": ticket.matricula_senior,
                "matricula_final": ticket.matricula_final,
                "n_tel_usuario": ticket.n_tel_usuario,
                "usuario_modelo": ticket.usuario_modelo,
                "ds_tipo_colaborador": ticket.ds_tipo_colaborador,
                "hub_novo_usu": ticket.hub_novo_usu,
                "unidade_novo_usu": ticket.unidade_novo_usu,
                "centro_custo": ticket.centro_custo,
                "cargo": ticket.cargo,
                "departamento_novo_usuario": ticket.departamento_novo_usuario,
                "ds_entidade": ticket.ds_entidade,
                "ds_acesso_solic": ticket.ds_acesso_solic,
                "cod_prest_mv": ticket.cod_prest_mv,
                "tipo_usuario": ticket.tipo_usuario,
                "ds_vinc_empr": ticket.ds_vinc_empr,
                "sigla_cp": ticket.sigla_cp,
                "registro_cp": ticket.registro_cp,
                "ds_tipo_cargo": ticket.ds_tipo_cargo,
                "dominio_email": ticket.dominio_email,
                "organizacao_dominio": ticket.organizacao_dominio,
                "ds_licenca": ticket.ds_licenca,
                "ds_custo_novo_usu": ticket.ds_custo_novo_usu,
                "ds_gestor": ticket.ds_gestor,
                "ds_email_gestor": ticket.ds_email_gestor,
                "ds_gerente": ticket.ds_gerente,
                "ds_email_gerente": ticket.ds_email_gerente,
                "aprovador_sap": ticket.aprovador_sap,
                "public_alvo": ticket.public_alvo,
                "obj_comunicacao": ticket.obj_comunicacao,
                "n_verba": ticket.n_verba,
                "ds_endereco": ticket.ds_endereco,
                "ds_obs": ticket.ds_obs,
                "resposta_chamado": ticket.resposta_chamado,
                "cod_change": ticket.cod_change
            }
            for ticket in tickets
        ]

        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@tickets_blueprint.route('/ticket-tasks', methods=['GET'])
def get_ticket_tasks():
    id = request.args.get('id')
    if not id:
        return jsonify({"error": "ID parameter is required"}), 400

    try:
        tasks = TbTicketsTasks.query.filter_by(cod_fluxo=id).all()

        if not tasks:
            return jsonify({"error": "No task found with the given ID"}), 404

        result = [
            {
                "id": task.id,
                "cod_task": task.cod_task,
                "cod_fluxo": task.cod_fluxo,
                "status": task.status,
                "descricao": task.descricao,
                "executor": task.executor,
                "aberto_por": task.aberto_por,
                "aberto_em": task.aberto_em,
                "execucao": task.execucao,
                "dt_fim": task.dt_fim,
                "tempo": task.tempo,
                "tempo_corrido": task.tempo_corrido,
                "dt_atual": task.dt_atual,
                "ds_concluido_por": task.ds_concluido_por,
                "ds_obs": task.ds_obs,
                "ticket_sap": task.ticket_sap,
                "ticket_solman": task.ticket_solman,
                "ds_anexo": task.ds_anexo,
                "email_criador_atividade": task.email_criador_atividade,
                "email_executor": task.email_executor,
                "tipo_atividade": task.tipo_atividade
            }
            for task in tasks
        ]

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500