from functools import wraps
from flask import request, jsonify
import jwt
import requests

ALLOWED_DOMAINS = [
    "angiocardis.com.br", "encore.com.br", "gastroclinicahospital.com.br", "grupooto.com.br", 
    "hmsm.com.br", "hospitalanchieta.com.br", "hospitalmeridional.com.br", "hospitalmeridionalsm.com.br", 
    "hospitalotoclinica.com.br", "hospitalpalmasmedical.com.br", "hospitalsaomateus.com.br", 
    "hsfdf.com.br", "hsmce.com.br", "hsp-saoluiz.com.br", "irtdf.com.br", "koracard.com.br", 
    "korasaude.com.br", "metropolitanoimagem.com.br", "neurologico.com.br", "otoimagem.com.br", 
    "otolab.med.br", "qualidadenasaude.com.br", "redemedical.com.br", "redemeridional.com.br", 
    "redeoto.com.br", "saofranciscodf.med.br", "saofranciscohospital.com.br", "idm.angiocardis.com.br", 
    "idm.encore.com.br", "idm.gastroclinicahospital.com.br", "idm.grupooto.com.br", "idm.hmsm.com.br", 
    "idm.hospitalanchieta.com.br", "idm.hospitalmeridional.com.br", "idm.hospitalotoclinica.com.br", 
    "idm.hospitalpalmasmedical.com.br", "idm.hospitalsaomateus.com.br", "idm.hsfdf.com.br", 
    "idm.hsmce.com.br", "idm.hsp-saoluiz.com.br", "idm.irtdf.com.br", "idm.koracard.com.br", 
    "seg.korasaude.com.br", "idm.korasaude.com.br", "idm.korsaude.com.br", "idm.metropolitanoimagem.com.br", 
    "idm.neurologico.com.br", "idm.otoimagem.com.br", "idm.otolab.med.br", "idm.qualidadenasaude.com.br", 
    "idm.redemedical.com.br", "idm.redemeridional.com.br", "idm.redeoto.com.br", "idm.saofranciscodf.med.br", 
    "idm.saofranciscohospital.com.br", "cadim.com.br", "seg.korasaude.com.br", "a2f.com.br", 
    "megawork.com", "mv.com.br", "qinetwork.com.br"
]

def get_google_public_keys():
    google_cert_url = "https://www.googleapis.com/oauth2/v3/certs"
    response = requests.get(google_cert_url)
    return response.json()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            token = auth_header.split(" ")[1]
            
        email = request.headers.get('X-User-Email')

        if not token or not email:
            return jsonify({'message': 'Token or X-User-Email is missing!'}), 401

        try:
            unverified_header = jwt.get_unverified_header(token)
            kid = unverified_header.get('kid')

            if not kid:
                return jsonify({'message': 'Invalid token header!'}), 401

            public_keys = get_google_public_keys()

            public_key = None
            for key in public_keys['keys']:
                if key['kid'] == kid:
                    public_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)
                    break

            if not public_key:
                return jsonify({'message': 'Public key not found!'}), 401
            
            decoded_token = jwt.decode(
                token, 
                public_key, 
                algorithms=['RS256'], 
                audience='759061524098-2lds7su9bpuoij6tapvq425s2hormnnd.apps.googleusercontent.com',
                options={"verify_exp": False}
            )

            if decoded_token.get('email') != email:
                return jsonify({'message': 'Access denied: Email does not match!'}), 403

            email_domain = email.split('@')[1]

            if email_domain not in ALLOWED_DOMAINS:
                return jsonify({'message': 'Access denied: Domain is not allowed!'}), 403

        except Exception as e:
            return jsonify({'message': f'Error during token validation: {str(e)}'}), 401

        return f(*args, **kwargs)

    return decorated