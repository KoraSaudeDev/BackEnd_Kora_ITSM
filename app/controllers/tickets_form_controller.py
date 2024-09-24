from flask import Blueprint, jsonify, request
from sqlalchemy import or_
from app import db
from app.models.vw_itsm_categoria import VwItsmCategoria
from app.models.vw_itsm_subcategoria import VwItsmSubcategoria
from app.models.vw_itsm_assunto import VwItsmAssunto
from app.models.vw_itsm_sla import VwItsmSla
from app.models.vw_hub import VwHub
from app.models.tb_unidade import TbUnidade
from app.models.tb_tickets_tasks_status import TbTicketsTasksStatus
from app.models.vw_dominios_email import VwDominiosEmail
from app.models.vw_itsm_destinatarios import VwItsmDestinatarios
from app.models.vw_areas_negocio import VwAreasNegocio
from app.models.vw_itsm_status_tickets import VwItsmStatusTickets
from app.models.vw_unidades import VwUnidades
from app.models.tb_centro_custo import TbCentroCusto
from app.models.tb_cargo import TbCargo
from app.models.tb_entidades import TbEntidades
from app.models.tb_ambiente_sap import TbAmbienteSap
from app.models.vw_perfis_sap import VwPerfisSap
from app.models.vw_tickets_motivo_sap import VwTicketsMotivoSap
from app.models.vw_areas_diretoria import VwAreasDiretoria
from app.models.tb_tipo_colaborador import TbTipoColaborador
from app.models.tb_licenca_google import TbLicencaGoogle
from app.models.tb_tipo_usuario import TbTipoUsuario
from app.models.vw_itsm_filas_emails import VwItsmFilasEmails
from app.models.tb_users_new import TbUsersNew

tickets_form_blueprint = Blueprint('tickets_form', __name__)

@tickets_form_blueprint.route('/categorias', methods=['GET'])
def get_all_categorias():
    try:
        categorias = VwItsmCategoria.query.all()
        result = [
            categoria.categoria for categoria in categorias
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@tickets_form_blueprint.route('/subcategorias', methods=['GET'])
def get_subcategorias_by_categoria():
    categoria = request.args.get('categoria')
    
    if not categoria:
        return jsonify([])

    try:
        subcategorias = VwItsmSubcategoria.query.filter_by(categoria=categoria).all()
        result = [
            subcategoria.subcategoria for subcategoria in subcategorias
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@tickets_form_blueprint.route('/assuntos', methods=['GET'])
def get_assuntos_by_categoria_subcategoria():
    categoria = request.args.get('categoria')
    subcategoria = request.args.get('subcategoria')
    
    if not categoria or not subcategoria:
        return jsonify([])

    try:
        assuntos = VwItsmAssunto.query.filter_by(categoria=categoria, subcategoria=subcategoria).all()
        result = [
            {
                "assunto": assunto.assunto,
                "prioridade": assunto.prioridade,
                "sla": assunto.sla,
                "tipo_assunto": assunto.tipo_assunto,
                "grupo_atendimento": assunto.grupo_atendimento
            } for assunto in assuntos
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@tickets_form_blueprint.route('/sla', methods=['GET'])
def get_all_slas():
    try:
        slas = VwItsmSla.query.all()
        result = [
            {
                "sla": sla.tempo,
                "prioridade": sla.prioridade,
                "descricao": sla.descricao,
                "tipo_tempo": sla.tipo_tempo
            }
            for sla in slas
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@tickets_form_blueprint.route('/hub', methods=['GET'])
def get_all_hubs():
    try:
        hubs = VwHub.query.all()
        result = [
            hub.HUB for hub in hubs
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@tickets_form_blueprint.route('/unidade', methods=['GET'])
def get_unidades_by_hub():
    hubs = request.args.get('hub')
    
    if not hubs:
        return jsonify([])
    
    hubs_list = hubs.split(',')
    
    try:
        query = db.session.query(TbUnidade.nu_hub, TbUnidade.st_razao_social).filter(
            TbUnidade.nu_hub.in_(hubs_list)
        ).distinct().order_by(TbUnidade.nu_hub)
        
        unidades = query.all()
        
        result = [
            f"{unidade.nu_hub}: {unidade.st_razao_social}" for unidade in unidades
        ]
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@tickets_form_blueprint.route('/usuarios-executores', methods=['GET'])
def get_all_usuarios_executores():
    try:
        filas = VwItsmDestinatarios.query.order_by(VwItsmDestinatarios.nome.asc()).all()
        result = [
            {
                "id": fila.id,
                "fila": fila.nome    
            }
            for fila in filas
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@tickets_form_blueprint.route('/email-fila', methods=['GET'])
def get_email_fila():
    id_fila = request.args.get('id_fila')
    unidade = request.args.get('unidade')

    if not id_fila or not unidade:
        return jsonify([])

    try:
        result = VwItsmFilasEmails.query.filter(
            VwItsmFilasEmails.id_fila == id_fila,
            or_(
                VwItsmFilasEmails.unidade == unidade,
                VwItsmFilasEmails.unidade.is_(None)
            )
        ).all()

        if result:
            data = [row.email for row in result]
            return jsonify(data), 200
        
        user_result = TbUsersNew.query.filter_by(id=id_fila).all()

        if user_result:
            user_emails = [user.ds_email for user in user_result if user.ds_email]
            return jsonify(user_emails), 200
        else:
            return jsonify([]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tickets_form_blueprint.route('/status', methods=['GET'])
def get_all_status():
    try:
        status = TbTicketsTasksStatus.query.order_by(TbTicketsTasksStatus.st_decricao.asc()).all()
        result = [
            stt.st_decricao for stt in status
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@tickets_form_blueprint.route('/status-tickets', methods=['GET'])
def get_all_status_tickets():
    try:
        status = VwItsmStatusTickets.query.order_by(VwItsmStatusTickets.nome.asc()).all()
        result = [
            stt.nome for stt in status
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@tickets_form_blueprint.route('/dominios-email', methods=['GET'])
def get_all_dominios_email():
    try:
        dominios = VwDominiosEmail.query.all()
        result = [
            {
                "dominio": dominio.dominio,
                "organizacao": dominio.organizacao
            }
            for dominio in dominios
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@tickets_form_blueprint.route('/areas-negocio', methods=['GET'])
def get_all_areas_negocio():
    try:
        areas_negocio = VwAreasNegocio.query.all()
        result = [
            area_negocio.Area_negocio for area_negocio in areas_negocio
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@tickets_form_blueprint.route('/unidade-novo-usu', methods=['GET'])
def get_unidades_novo_usu_by_hub():
    hubs = request.args.get('hub')
    
    if not hubs:
        return jsonify([])

    hubs_list = hubs.split(',')
    
    try:
        query = db.session.query(
            VwUnidades.hub, 
            VwUnidades.unidade_negocio,
            VwUnidades.sigla, 
            VwUnidades.cod_empresa
        ).filter(
            VwUnidades.hub.in_(hubs_list),
            VwUnidades.cod_empresa.isnot(None)
        ).distinct().order_by(VwUnidades.hub)

        unidades = query.all()
        
        result = [
            f"{unidade.sigla}: {unidade.unidade_negocio} - {unidade.cod_empresa}" for unidade in unidades
        ]

        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@tickets_form_blueprint.route('/centro-custo', methods=['GET'])
def get_centro_custo():
    cod_sap = request.args.get('cod_sap')
    
    if not cod_sap:
        return jsonify([])

    cod_list = cod_sap.split(',')
    
    try:
        query = db.session.query(
            TbCentroCusto.centro_custo,
            TbCentroCusto.descricao
        ).filter(
            TbCentroCusto.cod_empresa_sap.in_(cod_list)
        ).order_by(TbCentroCusto.descricao)

        centros_custo = query.all()
        
        result = [
            f"{centro.descricao} ({centro.centro_custo})" for centro in centros_custo
        ]

        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@tickets_form_blueprint.route('/cargo', methods=['GET'])
def get_all_cargos():
    try:
        cargps = TbCargo.query.order_by(TbCargo.cargo).all()
        result = [
            cargo.cargo for cargo in cargps
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@tickets_form_blueprint.route('/unidade-mv-tasy', methods=['GET'])
def get_unidade_mv_tasy():
    categoria = request.args.get('categoria')
    
    if not categoria:
        return jsonify([])

    try:
        entidades = (TbEntidades.query
                     .filter(TbEntidades.categoria == categoria)
                     .order_by(TbEntidades.sigla)
                     .all())
        
        result = [
            f"{entidade.sigla} ({entidade.estado})" if entidade.sigla != "CORPORATIVO" else f"{entidade.sigla}"
            for entidade in entidades
        ]
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@tickets_form_blueprint.route('/ambiente-sap', methods=['GET'])
def get_ambiente_sap():
    try:
        ambientes = (TbAmbienteSap.query
                     .filter(TbAmbienteSap.bl_ativo == 1)
                     .order_by(TbAmbienteSap.ds_ambiente)
                     .all())
        
        result = [
            ambiente.ds_ambiente for ambiente in ambientes
        ]
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@tickets_form_blueprint.route('/perfil-sap', methods=['GET'])
def get_perfil_sap():
    try:
        perfis = (VwPerfisSap.query
                     .order_by(VwPerfisSap.Perfil)
                     .all())
        
        result = [
            perfil.Perfil for perfil in perfis
        ]
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@tickets_form_blueprint.route('/motivo-sap', methods=['GET'])
def get_motivo_sap():
    try:
        motivos = (VwTicketsMotivoSap.query
                     .order_by(VwTicketsMotivoSap.ds_motivo)
                     .all())
        
        result = [
            motivo.ds_motivo for motivo in motivos
        ]
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@tickets_form_blueprint.route('/diretoria-sap', methods=['GET'])
def get_diretoria_sap():
    try:
        areas = (VwAreasDiretoria.query
                     .order_by(VwAreasDiretoria.ds_area)
                     .all())
        
        result = [
            area.ds_area for area in areas
        ]
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@tickets_form_blueprint.route('/tipo-colaborador', methods=['GET'])
def get_tipo_colaborador():
    try:
        tipos = (TbTipoColaborador.query
                     .filter(TbTipoColaborador.bl_ativo == 1)
                     .order_by(TbTipoColaborador.tipo)
                     .all())
        
        result = [
            tipo.tipo for tipo in tipos
        ]
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@tickets_form_blueprint.route('/licenca-google', methods=['GET'])
def get_licenca_google():
    try:
        licencas = (TbLicencaGoogle.query
                     .filter(TbLicencaGoogle.bl_ativo == 1)
                     .all())
        
        result = [
            licenca.licenca for licenca in licencas
        ]
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@tickets_form_blueprint.route('/tipo-usuario', methods=['GET'])
def get_tipo_usuario():
    try:
        tipos = (TbTipoUsuario.query
                     .filter(TbTipoUsuario.bl_ativo == 1)
                     .order_by(TbTipoUsuario.tipo)
                     .all())
        
        result = [
            tipo.tipo for tipo in tipos
        ]
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500