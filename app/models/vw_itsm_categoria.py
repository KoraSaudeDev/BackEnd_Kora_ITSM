from app import db

class VwItsmCategoria(db.Model):
    __tablename__ = 'VW_ITSM_CATEGORIA'

    id_categoria = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(255))