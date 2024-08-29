from app import db

class VwDominiosEmail(db.Model):
    __tablename__ = 'VW_DOMINIOS_EMAIL'

    id = db.Column(db.Integer, primary_key=True)
    dominio = db.Column(db.String(450))
    organizacao = db.Column(db.String(100))