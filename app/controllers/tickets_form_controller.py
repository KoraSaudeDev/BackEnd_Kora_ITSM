from flask import Blueprint, jsonify, request
from sqlalchemy import or_
from app import db
from app.models.vw_itsm_categoria import VwItsmCategoria
from app.models.vw_itsm_subcategoria import VwItsmSubcategoria
from app.models.vw_itsm_assunto import VwItsmAssunto
from app.models.vw_itsm_sla import VwItsmSla
from app.models.vw_hub import VwHub
from app.models.tb_unidade import TbUnidade
from app.models.vw_usuarios_executores import VwUsuariosExecutores
from app.models.tb_tickets_tasks_status import TbTicketsTasksStatus
from app.models.vw_dominios_email import VwDominiosEmail

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
        return jsonify({"error": "Categoria parameter is required"}), 400

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
        return jsonify({"error": "Both categoria and subcategoria parameters are required"}), 400

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
    hub = request.args.get('hub')
    
    if not hub:
        return jsonify({"error": "Hub parameter is required"}), 400
    
    try:
        query = db.session.query(TbUnidade.nu_hub, TbUnidade.st_razao_social).filter(TbUnidade.nu_hub == hub).distinct()
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
        usuarios = VwUsuariosExecutores.query.order_by(VwUsuariosExecutores.papel_nome.asc()).all()
        result = [
            usuario.papel_nome for usuario in usuarios
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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