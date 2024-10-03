import requests
from os import getenv
from dotenv import load_dotenv
from google.oauth2 import service_account
import google.auth.transport.requests

load_dotenv()

SERVICE_ACCOUNT_FILE = getenv('SERVICE_ACCOUNT_FILE')

def send_message_to_dm(space_name, message_text):
    """Função para enviar uma mensagem à DM no Google Chat"""
    url = f"https://chat.googleapis.com/v1/{space_name}/messages"
    headers = {
        "Authorization": f"Bearer {get_bot_access_token()}",
        "Content-Type": "application/json"
    }
    data = {
        "text": message_text
    }
    
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print("Mensagem enviada com sucesso!")
    else:
        print(f"Falha ao enviar mensagem: {response.status_code}, {response.text}")

def get_bot_access_token():
    """Função para obter o token OAuth 2.0 do bot usando uma conta de serviço"""
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=['https://www.googleapis.com/auth/chat.bot']
    )

    request = google.auth.transport.requests.Request()
    credentials.refresh(request)

    return credentials.token