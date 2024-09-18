from flask import Blueprint, jsonify, request, make_response
import requests
from google.oauth2 import service_account
import google.auth.transport.requests

chat_blueprint = Blueprint('chat', __name__)

@chat_blueprint.route('/', methods=['POST'])
def get_chat():
    data = request.get_json()

    if data.get('type') == 'ADDED_TO_SPACE' and data.get('space', {}).get('type') == 'DM':
        user_name = data.get('user', {}).get('displayName', 'Usuário')
        space_name = data.get('space', {}).get('name', 'Nome do espaço')
        print(space_name)
        
        welcome_message = (
            f"Olá {user_name}! 👋✨\n\n"
            "O chat comigo foi ativado com sucesso! A partir de agora, você receberá por aqui todas as atualizações dos seus tickets 🎫.\n\n"
            "Até breve e bons atendimentos! 💬✉️"
        )
        
        return jsonify({"text": welcome_message})

    elif data.get('type') == 'MESSAGE' and data.get('space', {}).get('type') == 'DM':
        info_message = (
            "Desculpe, eu sou apenas um bot de notificações. Não consigo responder a mensagens. 😉\n\n"
            "Você será notificado automaticamente aqui sobre atualizações de tickets 🎫."
        )
        
        return jsonify({"text": info_message})

    return make_response('', 204)

@chat_blueprint.route('/send', methods=['POST'])
def send_custom_message():
    data = request.get_json()
    
    space_name = data.get('space')
    message_text = data.get('message')
    
    if not space_name or not message_text:
        return jsonify({"error": "Espaço ou mensagem não fornecidos"}), 400
    
    send_message_to_dm(space_name, message_text)
    
    return jsonify({"message": "Mensagem enviada com sucesso!"}), 200

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
        'itsmkora-account-file.json',
        scopes=['https://www.googleapis.com/auth/chat.bot']
    )

    request = google.auth.transport.requests.Request()
    credentials.refresh(request)

    return credentials.token