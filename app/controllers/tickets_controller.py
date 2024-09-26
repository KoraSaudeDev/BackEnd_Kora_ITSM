from flask import Blueprint, jsonify, request
from sqlalchemy import or_, and_, asc, desc, distinct
import json
from datetime import datetime, time
from app import db
from app.models.tb_tickets import TbTickets
from app.models.tb_tickets_tasks import TbTicketsTasks
from app.models.tb_tickets_files import TbTicketsFiles
from app.models.tb_itsm_filtro_ma import TbItsmFiltroMa
from app.models.tb_itsm_filtro_me import TbItsmFiltroMe
from app.models.vw_itsm_sla import VwItsmSla

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
                "assunto": ticket.assunto,
                "ds_nivel": ticket.ds_nivel
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

@tickets_blueprint.route('/minha-equipe', methods=['POST'])
def get_minha_equipe():
    data = request.get_json()
    filas = data.get('filas', [])
    
    if len(filas) < 1:
        return jsonify({
            "page": 1,
            "pages": 1,
            "total_items": 0,
            "items_per_page": 10,
            "tickets": []
        })
     
    if not filas:
        return jsonify({"error": "Filas parameter is required"}), 400
 
    filtros = data.get('filtros', {})
    sort_orders = data.get('sort', {})
    
    date_filters = filtros.get('dateFilters', {})
    filter_options = filtros.get('filterOptions', {})
 
    cod_fluxo = request.args.get('cod_fluxo', None)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    try:
        slas = VwItsmSla.query.all()
        sla_mapping = {sla.prioridade: sla.descricao for sla in slas}
        
        in_conditions = TbTickets.executor.in_(filas)
        
        query = TbTickets.query.filter(
            in_conditions,
            TbTickets.status.notin_(["Finalizado", "Cancelado"])
        )
        
        for column, dates in date_filters.items():
            start_date = dates.get('startDate')
            end_date = dates.get('endDate')
            
            if start_date and end_date:
                if isinstance(start_date, datetime):
                    start_date = start_date.replace(hour=0, minute=0, second=0)
                else:
                    start_date = datetime.strptime(start_date, '%Y-%m-%d').replace(hour=0, minute=0, second=0)
                
                if isinstance(end_date, datetime):
                    end_date = end_date.replace(hour=23, minute=59, second=59)
                else:
                    end_date = datetime.strptime(end_date, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
                
                column_attr = getattr(TbTickets, column, None)
                if column_attr:
                    query = query.filter(and_(
                        column_attr >= start_date,
                        column_attr <= end_date
                    ))

        for column, values in filter_options.items():
            column_attr = getattr(TbTickets, column, None)
            if column_attr and isinstance(values, list):
                query = query.filter(column_attr.in_(values))

        if cod_fluxo:
            query = query.filter(TbTickets.cod_fluxo.like(f"%{cod_fluxo}%"))

        sort_by_columns = []

        if sort_orders:
            for col, order in sort_orders.items():
                if hasattr(TbTickets, col):
                    column_attr = getattr(TbTickets, col)
                    if order.lower() == 'desc':
                        sort_by_columns.append(desc(column_attr))
                    else:
                        sort_by_columns.append(asc(column_attr))

        if not any(col == 'abertura' for col in sort_orders):
            sort_by_columns.append(desc(TbTickets.abertura))

        if sort_by_columns:
            query = query.order_by(*sort_by_columns)

        paginated_tickets = query.paginate(page=page, per_page=per_page, error_out=False)

        results = []
        for ticket in paginated_tickets.items:
            sla_description = sla_mapping.get(ticket.ds_nivel, "N/A")
            prioridade_descricao = f"{ticket.ds_nivel} - {sla_description}"
            
            results.append({
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
                "ds_nivel": ticket.ds_nivel,
                "prioridadeDescricao": prioridade_descricao
            })

        return jsonify({
            "page": paginated_tickets.page,
            "pages": paginated_tickets.pages,
            "total_items": paginated_tickets.total,
            "items_per_page": paginated_tickets.per_page,
            "tickets": results
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@tickets_blueprint.route('/meus-atendimentos', methods=['POST'])
def get_meus_atendimentos():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User_id parameter is required"}), 400

    data = request.get_json()
    filtros = data.get('filtros', {})
    sort_orders = data.get('sort', {})
    
    date_filters = filtros.get('dateFilters', {})
    filter_options = filtros.get('filterOptions', {})
    
    cod_fluxo = request.args.get('cod_fluxo', None)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    try:
        slas = VwItsmSla.query.all()
        sla_mapping = {sla.prioridade: sla.descricao for sla in slas}
        
        query = TbTickets.query.filter(
            TbTickets.executor == user_id,
            TbTickets.status.notin_(["Finalizado", "Cancelado"])
        )

        for column, dates in date_filters.items():
            start_date = dates.get('startDate')
            end_date = dates.get('endDate')
            
            if start_date and end_date:
                if isinstance(start_date, datetime):
                    start_date = start_date.replace(hour=0, minute=0, second=0)
                else:
                    start_date = datetime.strptime(start_date, '%Y-%m-%d').replace(hour=0, minute=0, second=0)
                
                if isinstance(end_date, datetime):
                    end_date = end_date.replace(hour=23, minute=59, second=59)
                else:
                    end_date = datetime.strptime(end_date, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
                
                column_attr = getattr(TbTickets, column, None)
                if column_attr:
                    query = query.filter(and_(
                        column_attr >= start_date,
                        column_attr <= end_date
                    ))

        for column, values in filter_options.items():
            column_attr = getattr(TbTickets, column, None)
            if column_attr and isinstance(values, list):
                query = query.filter(column_attr.in_(values))

        if cod_fluxo:
            query = query.filter(TbTickets.cod_fluxo.like(f"%{cod_fluxo}%"))

        sort_by_columns = []

        if sort_orders:
            for col, order in sort_orders.items():
                if hasattr(TbTickets, col):
                    column_attr = getattr(TbTickets, col)
                    if order.lower() == 'desc':
                        sort_by_columns.append(desc(column_attr))
                    else:
                        sort_by_columns.append(asc(column_attr))

        if not any(col == 'abertura' for col in sort_orders):
            sort_by_columns.append(desc(TbTickets.abertura))

        if sort_by_columns:
            query = query.order_by(*sort_by_columns)

        paginated_tickets = query.paginate(page=page, per_page=per_page, error_out=False)

        results = []
        for ticket in paginated_tickets.items:
            sla_description = sla_mapping.get(ticket.ds_nivel, "N/A")
            prioridade_descricao = f"{ticket.ds_nivel} - {sla_description}"
            
            results.append({
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
                "ds_nivel": ticket.ds_nivel,
                "prioridadeDescricao": prioridade_descricao
            })

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
    parametro = request.args.get('p')
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    try:
        query = TbTickets.query

        if parametro:
            if parametro.isdigit():
                query = query.filter(
                    TbTickets.cod_fluxo == parametro
                )
            else:
                query = query.filter(
                    or_(
                        TbTickets.nome.like(f'%{parametro}%'),
                        TbTickets.email_solicitante.like(f'%{parametro}%'),
                        TbTickets.descricao.like(f'%{parametro}%')
                    )
                )
        
        query = query.order_by(TbTickets.cod_fluxo.desc())
        
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
                "ds_nivel": ticket.ds_nivel
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
        ticket = TbTickets.query.filter_by(cod_fluxo=cod_fluxo).first()

        if ticket:
            result = {
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
                "tempo_minutos": ticket.tempo_minutos,
                "tempo_minutos_corridos": ticket.tempo_minutos_corridos,
                "ds_nivel": ticket.ds_nivel,
                "grupo": ticket.grupo,
                "executor": ticket.executor,
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
                "anexo": ticket.anexo,
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
                "empresa_colab_cadastrado": ticket.empresa_colab_cadastrado,
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
                "material_referencia": ticket.material_referencia,
                "urgencia": ticket.urgencia,
                "ds_endereco": ticket.ds_endereco,
                "email_receb_alias": ticket.email_receb_alias,
                "endereco_alias": ticket.endereco_alias,
                "ds_obs": ticket.ds_obs,
                "resposta_chamado": ticket.resposta_chamado,
                "anexo_resposta": ticket.anexo_resposta,
                "cod_change": ticket.cod_change,
                "ctrl_criacao_usuario": ticket.ctrl_criacao_usuario,
                "cod_empresa": ticket.cod_empresa,
                "telefone_empresa": ticket.telefone_empresa,
                "Endereco": ticket.Endereco,
                "Site": ticket.Site,
                "Pais": ticket.Pais,
                "CEP": ticket.CEP,
                "Estado": ticket.Estado,
                "Cidade": ticket.Cidade,
                "Logon_Script": ticket.Logon_Script,
                "Nome_Empresa": ticket.Nome_Empresa
            }

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@tickets_blueprint.route('/ticket-tasks', methods=['GET'])
def get_ticket_tasks():
    id = request.args.get('id')
    if not id:
        return jsonify({"error": "ID parameter is required"}), 400

    try:
        tasks = TbTicketsTasks.query.filter_by(cod_fluxo=id).all()

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

@tickets_blueprint.route('/ticket-files', methods=['GET'])
def get_ticket_files():
    id = request.args.get('id')
    if not id:
        return jsonify({"error": "ID parameter is required"}), 400

    try:
        files = TbTicketsFiles.query.filter_by(cod_fluxo=id).all()

        result = [
            {
                "id": file.id,
                "cod_anexo": file.cod_anexo,
                "cod_fluxo": file.cod_fluxo,
                "ds_texto": file.ds_texto,
                "ds_anexo": file.ds_anexo,
                "ds_adicionado_por": file.ds_adicionado_por,
                "abertura": file.abertura
            }
            for file in files
        ]

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@tickets_blueprint.route('/filtro-ma/<user_id>', methods=['GET'])
def get_filtro_ma(user_id):
    try:
        existing_filtro = TbItsmFiltroMa.query.filter_by(id_user=user_id).first()
        if existing_filtro:
            filtro_data = json.loads(existing_filtro.filtro)
            return jsonify(filtro_data), 200
        else:
            return jsonify([])

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@tickets_blueprint.route('/filtro-me/<user_id>', methods=['GET'])
def get_filtro_me(user_id):
    try:
        existing_filtro = TbItsmFiltroMe.query.filter_by(id_user=user_id).first()
        if existing_filtro:
            filtro_data = json.loads(existing_filtro.filtro)
            return jsonify(filtro_data), 200
        else:
            return jsonify([])

    except Exception as e:
        return jsonify({"error": str(e)}), 500