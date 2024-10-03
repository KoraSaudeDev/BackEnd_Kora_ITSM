import os
from os import getenv
from dotenv import load_dotenv
import threading
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from werkzeug.utils import secure_filename
from app.utils.auth_utils import token_required

load_dotenv()
file_lock = threading.Lock()

TICKETS_FOLDER_ID = getenv('FOLDER_ANEXOS_TICKETS_ID')
SERVICE_ACCOUNT_FILE = getenv('SERVICE_ACCOUNT_FILE')
SCOPES = ['https://www.googleapis.com/auth/drive']

credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=credentials)

GDRIVE_FOLDERS = {
    1: {
        "files": "tb_tickets_Files_", 
        "images": "tb_tickets_Images"
    },
    2: {
        "files": "tb_tickets_tasks_Files_", 
        "images": "tb_tickets_tasks_Images"
    },
    3: {
        "files": "tb_tickets_files_Files_", 
        "images": "tb_tickets_files_Images"
    }
}

def get_id_from_path(folder_id, file_path):
    try:
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
    except Exception as e:
        print(f"Erro ao obter o ID do arquivo: {str(e)}")
        return None

def upload_file_gdrive(path_local, name, path_google):
    try:
        if not os.path.exists(path_local):
            return {"error": f"File not found: {path_local}"}
        
        destination_folder_id = get_id_from_path(TICKETS_FOLDER_ID, path_google)
        
        if not destination_folder_id:
            return {"error": f"Destination folder not found -> {path_google}"}
        
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
        
        return {"id": file.get('id')}
    except Exception as e:
        return {"error": "An error occurred during file upload", "details": str(e)}

def async_upload(file_path, new_filename, gdrive_folder):
    try:
        with file_lock:
            gdrive_response = upload_file_gdrive(path_local=file_path, name=new_filename, path_google=gdrive_folder)

        if 'id' in gdrive_response:
            print(f"Arquivo inserido no Google Drive: {gdrive_response['id']}")
            try:
                os.remove(file_path)
                print(f"Arquivo local removido: {file_path}")
            except Exception as e:
                print(f"Erro ao remover o arquivo local: {file_path}. Detalhes: {e}")
        else:
            print("Falha ao fazer upload do arquivo para o Google Drive. Detalhes:", gdrive_response.get('error'))
    except Exception as e:
        print(f"An error occurred while uploading the file: {e}")