from functools import wraps
from flask import request, jsonify
import jwt

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
            decoded_token = jwt.decode(token, options={"verify_signature": False})

            if decoded_token.get('email') != email:
                return jsonify({'message': 'Access denied: Email does not match!'}), 403

            email_domain = email.split('@')[1]

            if email_domain not in ALLOWED_DOMAINS:
                return jsonify({'message': 'Access denied: Domain is not allowed!'}), 403

        except ValueError:
            return jsonify({'message': 'Invalid token!'}), 401

        return f(*args, **kwargs)

    return decorated