from app import db

class VwItsmDestinatarios(db.Model):
    __tablename__ = 'VW_ITSM_DESTINATARIOS'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255))