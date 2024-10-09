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

@wf_po_update_blueprint.route('/wf-po/<int:id>', methods=['PATCH'])
@token_required
def update_requisicao(id):
    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        req = TbWFPO.query.get(id)
        if not req:
            return jsonify({"error": "Requisição WF-PO not found"}), 404

        for key, value in data.items():
            if hasattr(req, key):
                setattr(req, key, value)
            else:
                return jsonify({"error": f"Invalid field: {key}"}), 400

        db.session.commit()

        return jsonify({"message": "Requisição WF-PO updated successfully"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@wf_po_update_blueprint.route('/wf-po-material/<int:id>', methods=['PATCH'])
@token_required
def update_materiais(id):
    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        material = TbWFPOMateriais.query.get(id)
        if not material:
            return jsonify({"error": "Material not found"}), 404

        for key, value in data.items():
            if hasattr(material, key):
                setattr(material, key, value)
            else:
                return jsonify({"error": f"Invalid field: {key}"}), 400

        db.session.commit()

        return jsonify({"message": "Material updated successfully"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@wf_po_update_blueprint.route('/wf-po-task/<int:id>', methods=['PATCH'])
@token_required
def update_wf_po_task(id):
    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        task = TbWFPOTasks.query.get(id)
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