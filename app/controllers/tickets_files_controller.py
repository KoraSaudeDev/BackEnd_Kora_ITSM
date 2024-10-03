from flask import Blueprint, jsonify, request
import os
from os import getenv
from dotenv import load_dotenv
import imghdr
import random
import threading
from werkzeug.utils import secure_filename
from app.utils.auth_utils import token_required
from app.utils.files_utils import get_id_from_path, async_upload, GDRIVE_FOLDERS, TICKETS_FOLDER_ID

load_dotenv()
file_lock = threading.Lock()

UPLOAD_FOLDER = getenv('UPLOAD_FOLDER_LOCAL')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

tickets_files_blueprint = Blueprint('tickets_files_blueprint', __name__)

@tickets_files_blueprint.route('/upload', methods=['POST'])
@token_required
def upload_file_local():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo foi enviado'}), 400

        file = request.files['file']
        upload_type = request.form.get('uploadType')

        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400

        if not upload_type:
            return jsonify({'error': 'uploadType não fornecido'}), 400

        upload_type = int(upload_type)
        
        random_prefix = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        filename = secure_filename(file.filename)
        new_filename = f"{random_prefix}_{filename}"

        file_path = os.path.join(UPLOAD_FOLDER, new_filename)
        
        with file_lock:
            file.save(file_path)
        
        is_image = imghdr.what(file_path)

        if is_image:
            gdrive_folder = GDRIVE_FOLDERS[upload_type]["images"]
        else:
            gdrive_folder = GDRIVE_FOLDERS[upload_type]["files"]
        
        response = jsonify({'message': 'Upload iniciado com sucesso!', 'filename': f"{gdrive_folder}/{new_filename}"})
        response.status_code = 202

        threading.Thread(target=async_upload, args=(file_path, new_filename, gdrive_folder)).start()

        return response
    except Exception as e:
        return jsonify({"error": "An error occurred while processing the upload", "details": str(e)}), 500

@tickets_files_blueprint.route('/open-url', methods=['GET'])
@token_required
def get_open_url():
    try:
        path = request.args.get('path')
        if not path:
            return jsonify({"error": "Path parameter is required"}), 400
        
        file_id = get_id_from_path(TICKETS_FOLDER_ID, path)
        if not file_id:
            return jsonify({"error": "File not found"}), 404
        
        return f"https://drive.google.com/file/d/{file_id}/preview"

    except Exception as e:
        return jsonify({"error": "An error occurred while processing your request", "details": str(e)}), 500

@tickets_files_blueprint.route('/download-url', methods=['GET'])
@token_required
def get_download_url():
    try:
        path = request.args.get('path')
        if not path:
            return jsonify({"error": "Path parameter is required"}), 400
        
        file_id = get_id_from_path(TICKETS_FOLDER_ID, path)
        if not file_id:
            return jsonify({"error": "File not found"}), 404
        
        return f"https://drive.google.com/uc?id={file_id}&export=download"

    except Exception as e:
        return jsonify({"error": "An error occurred while processing your request", "details": str(e)}), 500