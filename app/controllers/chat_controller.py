from flask import Blueprint, jsonify, request, make_response
from os import getenv
from app.utils.chat_utils import send_message_to_dm

SERVICE_ACCOUNT_FILE = getenv('SERVICE_ACCOUNT_FILE')

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