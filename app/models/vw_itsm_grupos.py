from app import db

class VwItsmGrupos(db.Model):
    __tablename__ = 'VW_ITSM_GRUPOS'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    id_grupo = db.Column(db.Integer)
    grupo = db.Column(db.String(255))
    id_papel = db.Column(db.Integer)
    papel = db.Column(db.String(255))