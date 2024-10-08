from flask import Blueprint, jsonify, request
import requests
import json
from app import db
from sqlalchemy.exc import SQLAlchemyError
from app.models.tb_wf_po import TbWFPO
from app.models.tb_wf_po_materiais import TbWFPOMateriais
from app.models.tb_wf_po_tasks import TbWFPOTasks
from app.models.tb_wf_po_aprovacoes import TbWFPOAprovacoes
from app.models.tb_wf_po_bionexo import TbWFPOBionexo
from app.utils.auth_utils import token_required

wf_po_update_blueprint = Blueprint('wf_po_update', __name__)

@wf_po_update_blueprint.route('/wf-po', methods=['POST'])
@token_required
def create_requisicao():
    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        req = TbWFPO(**data)

        db.session.add(req)
        db.session.commit()

        return jsonify({"message": "WF-PO created successfully", "id": req.id}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@wf_po_update_blueprint.route('/wf-po-material', methods=['POST'])
@token_required
def create_materiais():
    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        material = TbWFPOMateriais(**data)

        db.session.add(material)
        db.session.commit()

        return jsonify({"message": "Material created successfully", "id": material.id}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@wf_po_update_blueprint.route('/wf-po-task', methods=['POST'])
@token_required
def create_task():
    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        task = TbWFPOTasks(**data)

        db.session.add(task)
        db.session.commit()

        return jsonify({"message": "Task created successfully", "id": task.id}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@wf_po_update_blueprint.route('/wf-po-aprovacao', methods=['POST'])
@token_required
def create_aprovacao():
    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        aprovacao = TbWFPOAprovacoes(**data)

        db.session.add(aprovacao)
        db.session.commit()

        return jsonify({"message": "Aprovação created successfully", "id": aprovacao.id}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@wf_po_update_blueprint.route('/wf-po-bionexo', methods=['POST'])
@token_required
def create_bionexo_log():
    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        bio = TbWFPOBionexo(**data)

        db.session.add(bio)
        db.session.commit()

        return jsonify({"message": "Bionexo log created successfully", "id": bio.id}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500