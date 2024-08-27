from flask import Blueprint, jsonify, request
from sqlalchemy import or_
import os
from os import getenv
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

load_dotenv()

TICKETS_FOLDER_ID = getenv('FOLDER_ANEXOS_TICKETS_ID')
SERVICE_ACCOUNT_FILE = getenv('SERVICE_ACCOUNT_FILE')
SCOPES = ['https://www.googleapis.com/auth/drive']

credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=credentials)

tickets_files_blueprint = Blueprint('tickets_files_blueprint', __name__)

@tickets_files_blueprint.route('/upload', methods=['GET'])
def upload_file():
    path_local = request.args.get('path_local')
    if not path_local:
        return jsonify({"error": "Path_local parameter is required"}), 400
    
    if not os.path.exists(path_local):
        return jsonify({"error": f"File not found: {path_local}"}), 404
    
    name = request.args.get('name')
    if not name:
        return jsonify({"error": "Name parameter is required"}), 400
    
    path_google = request.args.get('path_google')
    if not path_google:
        return jsonify({"error": "Path_google parameter is required"}), 400
    
    destination_folder_id = get_id_from_path(TICKETS_FOLDER_ID, path_google)
    
    if not destination_folder_id:
        return jsonify({"error": f"Destination folder not found -> {path_google}"}), 404
    
    file_metadata = {
        'name': name,
        'parents': [destination_folder_id]
    }
    
    media = MediaFileUpload(path_local, resumable=True)
    file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    
    return file.get('id')

@tickets_files_blueprint.route('/open-url', methods=['GET'])
def get_open_url():
    path = request.args.get('path')
    if not path:
        return jsonify({"error": "Path parameter is required"}), 400
    
    file_id = get_id_from_path(TICKETS_FOLDER_ID, path)
    
    return f"https://drive.google.com/file/d/{file_id}/preview"

@tickets_files_blueprint.route('/download-url', methods=['GET'])
def get_download_url():
    path = request.args.get('path')
    if not path:
        return jsonify({"error": "Path parameter is required"}), 400
    
    file_id = get_id_from_path(TICKETS_FOLDER_ID, path)
    
    return f"https://drive.google.com/uc?id={file_id}&export=download"

def get_id_from_path(folder_id, file_path):
    parts = file_path.split('/')
    current_folder_id = folder_id

    for part in parts[:-1]:
        query = f"'{current_folder_id}' in parents and name = '{part}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
        results = drive_service.files().list(q=query, fields="files(id, name)").execute()
        items = results.get('files', [])
        
        if not items:
            print(f"Subpasta '{part}' não encontrada.")
            return None
        else:
            current_folder_id = items[0]['id']

    file_name = parts[-1]
    query = f"'{current_folder_id}' in parents and name = '{file_name}' and trashed = false"
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    items = results.get('files', [])
    
    if not items:
        print('Arquivo não encontrado.')
        return None
    else:
        return items[0]['id']