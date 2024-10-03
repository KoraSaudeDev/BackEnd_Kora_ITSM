from flask import Blueprint, jsonify, request
import requests
from google.oauth2 import id_token
from google.auth.transport import requests
from app.utils.auth_utils import ALLOWED_DOMAINS

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/verify-token', methods=['POST'])
def verify_token():
    token = request.headers.get('Authorization').split('Bearer ')[1]

    try:
        id_info = id_token.verify_oauth2_token(token, requests.Request(), '759061524098-2lds7su9bpuoij6tapvq425s2hormnnd.apps.googleusercontent.com')

        domain = id_info.get('hd')
        if domain in ALLOWED_DOMAINS:
            return jsonify({'message': 'Token válido e domínio autorizado', 'user': id_info})
        else:
            return jsonify({'error': 'Unauthorized domain'}), 401
    except ValueError as e:
        return jsonify({'error': 'Invalid token', 'message': str(e)}), 401