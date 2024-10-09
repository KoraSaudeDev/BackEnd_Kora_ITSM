import os
from os import getenv
from dotenv import load_dotenv
import threading
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from werkzeug.utils import secure_filename
from app.utils.auth_utils import token_required
from flask_mail import Message
from app import mail

load_dotenv()
file_lock = threading.Lock()

TICKETS_FOLDER_ID = getenv('FOLDER_ANEXOS_TICKETS_ID')
SERVICE_ACCOUNT_FILE = getenv('SERVICE_ACCOUNT_FILE')
SCOPES = ['https://www.googleapis.com/auth/drive']

credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=credentials)

GDRIVE_FOLDERS = {
    1: {
        "files": {
            "name": "tb_tickets_Files_", 
            "id": "1mxvewLAgyDeUQIKV0z-pGYhLd05812Kr"
        }, 
        "images": {
            "name": "tb_tickets_Images", 
            "id": "1-sBHBoVdkWqpvhqhXEYmo8zE13iF8oyd"
        }
    },
    2: {
        "files": {
            "name": "tb_tickets_tasks_Files_", 
            "id": "1pfPp3Lmpdymog7Y54pj2oBnmSti4GJba"
        }, 
        "images": {
            "name": "tb_tickets_tasks_Images", 
            "id": "1Mj5tyuvwesIeLncsyez_qkyMKtnv5x9L"
        }
    },
    3: {
        "files": {
            "name": "tb_tickets_files_Files_", 
            "id": "1Tbe8E7yoR73CrmQLOPtK0LrFv5VlGgV2"
        }, 
        "images": {
            "name": "tb_tickets_files_Images", 
            "id": "1mFxr6cHuUZ5UmU9_91XM2nnc0Xu1ygQ7"
        }
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

def upload_file_gdrive(path_local, name, path_google, folder_type, is_image):
    try:
        if not os.path.exists(path_local):
            return {"error": f"File not found: {path_local}"}
        
        folder_info = GDRIVE_FOLDERS.get(folder_type, {})
        if is_image:
            destination_folder_id = folder_info['images']['id'] if folder_info else None
        else:
            destination_folder_id = folder_info['files']['id'] if folder_info else None
        
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
        
        return {"id": file.get('id'), "folder": path_google}
    except Exception as e:
        return {"error": "An error occurred during file upload", "details": str(e)}

def async_upload(file_path, new_filename, gdrive_folder, folder_type, is_image):
    try:
        with file_lock:
            gdrive_response = upload_file_gdrive(path_local=file_path, name=new_filename, path_google=gdrive_folder, folder_type=folder_type, is_image=is_image)

        if 'id' in gdrive_response:
            print(f"Arquivo inserido no Google Drive: {gdrive_response['id']} - Pasta: {gdrive_response['folder']}")
            try:
                os.remove(file_path)
                print(f"Arquivo local removido: {file_path}")
            except Exception as e:
                print(f"Erro ao remover o arquivo local: {file_path}. Detalhes: {e}")
        else:
            print("Falha ao fazer upload do arquivo para o Google Drive. Detalhes:", gdrive_response.get('error'))
            subject = "Erro no upload para o Google Drive"
            recipients = ["pedro.magalhaes@korasaude.com.br"]
            body = f"Ocorreu um erro ao fazer o upload do arquivo {file_path}\nPasta: {gdrive_folder}\nDetalhes: {gdrive_response.get('error')}"
            send_error_email_with_attachment(subject, recipients, body, file_path)
    except Exception as e:
        print(f"An error occurred while uploading the file: {e}")
        subject = "Erro inesperado no upload para o Google Drive"
        recipients = ["pedro.magalhaes@korasaude.com.br"]
        body = f"Ocorreu um erro inesperado ao fazer o upload do arquivo {file_path}\nPasta: {gdrive_folder}\nDetalhes: {e}"
        send_error_email_with_attachment(subject, recipients, body, file_path)
        
def send_error_email_with_attachment(subject, recipients, body, attachment_path):
    from app import create_app
    app = create_app()

    try:
        with app.app_context():
            msg = Message(subject=subject,
                          recipients=recipients,
                          body=body)

            try:
                with open(attachment_path, 'rb') as file:
                    msg.attach(filename=os.path.basename(attachment_path),
                               content_type='application/octet-stream',
                               data=file.read())
                
                mail.send(msg)
                print(f"Email enviado com o anexo: {attachment_path}")

            except Exception as attachment_error:
                print(f"Erro ao anexar o arquivo: {attachment_path}. Detalhes: {attachment_error}")

                body += f"\n\nOcorreu um erro ao anexar o arquivo '{os.path.basename(attachment_path)}'. O arquivo não foi enviado em anexo devido ao erro: {attachment_error}"
                
                msg = Message(subject=subject,
                              recipients=recipients,
                              body=body)

                mail.send(msg)
                print("Email enviado sem o anexo devido ao erro.")

    except Exception as e:
        print(f"Erro ao enviar email. Detalhes: {e}")
