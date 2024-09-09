from app import db

class VwItsmFilasGestores(db.Model):
    __tablename__ = 'VW_ITSM_FILAS_GESTORES'

    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer)
    nome = db.Column(db.String(255))
    email = db.Column(db.String(150))
    id_fila = db.Column(db.Integer)
    fila = db.Column(db.String(255))
    created_at = db.Column(db.DateTime)