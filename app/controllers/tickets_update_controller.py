import uuid
from flask import Blueprint, jsonify, request
import requests
import json
from os import getenv
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError
from app.models.tb_tickets import TbTickets
from app.models.tb_tickets_tasks import TbTicketsTasks
from app.models.tb_tickets_files import TbTicketsFiles
from app.models.tb_itsm_log import TbItsmLog
from app.models.tb_itsm_filtro_ma import TbItsmFiltroMa
from app.models.tb_itsm_filtro_me import TbItsmFiltroMe
from app import db
from app.utils.auth_utils import token_required

load_dotenv()

tickets_update_blueprint = Blueprint('tickets_update', __name__)

@tickets_update_blueprint.route('/<int:cod_fluxo>', methods=['PATCH'])
@token_required
def update_ticket(cod_fluxo):
    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        ticket = TbTickets.query.get(cod_fluxo)
        if not ticket:
            return jsonify({"error": "Ticket not found"}), 404

        for key, value in data.items():
            if hasattr(ticket, key):
                setattr(ticket, key, value)
            else:
                return jsonify({"error": f"Invalid field: {key}"}), 400

        db.session.commit()

        return jsonify({"message": "Ticket updated successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@tickets_update_blueprint.route('/task/<int:cod_task>', methods=['PATCH'])
@token_required
def update_task(cod_task):
    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        task = TbTicketsTasks.query.get(cod_task)
        if not task:
            return jsonify({"error": "Task not found"}), 404

        for key, value in data.items():
            if hasattr(task, key):
                setattr(task, key, value)
            else:
                return jsonify({"error": f"Invalid field: {key}"}), 400

        db.session.commit()

        return jsonify({"message": "Task updated successfully"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@tickets_update_blueprint.route('/task', methods=['POST'])
@token_required
def create_task():
    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        if 'id' not in data or not data['id']:
            data['id'] = str(uuid.uuid4())

        new_task = TbTicketsTasks(**data)

        db.session.add(new_task)
        db.session.commit()

        return jsonify({"message": "Task created successfully", "task_id": new_task.cod_task}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@tickets_update_blueprint.route('/file', methods=['POST'])
@token_required
def create_file():
    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        if 'id' not in data or not data['id']:
            data['id'] = str(uuid.uuid4())

        new_file = TbTicketsFiles(**data)

        db.session.add(new_file)
        db.session.commit()

        return jsonify({"message": "File created successfully", "anexo_id": new_file.cod_anexo}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@tickets_update_blueprint.route('/log', methods=['POST'])
@token_required
def create_log():
    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        new_log = TbItsmLog(**data)

        db.session.add(new_log)
        db.session.commit()

        return jsonify({"message": "Log created successfully"}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@tickets_update_blueprint.route('/filtro-ma', methods=['POST'])
@token_required
def create_update_filtro_ma():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User_id parameter is required"}), 400
    
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        json_data = json.dumps(data)
        existing_filtro = TbItsmFiltroMa.query.filter_by(id_user=user_id).first()
        
        if existing_filtro:
            existing_filtro.filtro = json_data
            db.session.commit()
            return jsonify("Filtro updated successfully"), 200
        else:
            filtro = TbItsmFiltroMa(id_user=user_id, filtro=json_data)
            db.session.add(filtro)
            db.session.commit()
            return jsonify("Filtro created successfully"), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@tickets_update_blueprint.route('/delete-filtro-ma', methods=['POST'])
@token_required
def delete_filtro_ma():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User_id parameter is required"}), 400
    
    try:
        existing_filtro = TbItsmFiltroMa.query.filter_by(id_user=user_id).first()
        
        if existing_filtro:
            db.session.delete(existing_filtro)
            db.session.commit()
            return jsonify("Filtro deleted successfully")
        else:
            return jsonify("User does not have a filter")

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@tickets_update_blueprint.route('/filtro-me', methods=['POST'])
@token_required
def create_update_filtro_me():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User_id parameter is required"}), 400
    
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        json_data = json.dumps(data)
        existing_filtro = TbItsmFiltroMe.query.filter_by(id_user=user_id).first()
        
        if existing_filtro:
            existing_filtro.filtro = json_data
            db.session.commit()
            return jsonify("Filtro updated successfully"), 200
        else:
            filtro = TbItsmFiltroMe(id_user=user_id, filtro=json_data)
            db.session.add(filtro)
            db.session.commit()
            return jsonify("Filtro created successfully"), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@tickets_update_blueprint.route('/delete-filtro-me', methods=['POST'])
@token_required
def delete_filtro_me():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User_id parameter is required"}), 400
    
    try:
        existing_filtro = TbItsmFiltroMe.query.filter_by(id_user=user_id).first()
        
        if existing_filtro:
            db.session.delete(existing_filtro)
            db.session.commit()
            return jsonify("Filtro deleted successfully")
        else:
            return jsonify("User does not have a filter")

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@tickets_update_blueprint.route('/create-user-google', methods=['POST'])
@token_required
def create_google_user():
    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        url = f"{getenv('URL_GCP_KORA_API')}/create"
        
        headers = {}

        response = requests.post(url, headers=headers, data=data).json()
        
        return jsonify(response)

    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

@tickets_update_blueprint.route('/sla', methods=['POST'])
@token_required
def update_sla_status():
    cod_fluxo = request.args.get('cod_fluxo')

    if not cod_fluxo:
        return jsonify({"error": "Cod_fluxo parameter is required"}), 400

    try:
        url = f"{getenv('URL_GCP_KORA_API')}/sla"

        payload = json.dumps({
            "cod_fluxo": cod_fluxo,
            "N° Ticket": cod_fluxo
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.post(url, headers=headers, data=payload).json()
        
        return jsonify(response)

    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500