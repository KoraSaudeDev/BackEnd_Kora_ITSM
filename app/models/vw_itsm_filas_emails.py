from app import db

class VwItsmFilasEmails(db.Model):
    __tablename__ = 'VW_ITSM_FILAS_EMAILS'

    id = db.Column(db.Integer, primary_key=True)
    id_fila = db.Column(db.Integer)
    fila = db.Column(db.String(255))
    email = db.Column(db.String(255))
    unidade = db.Column(db.String(255))