from app import db

class VwWFPOUsuarios(db.Model):
    __tablename__ = 'VW_WF_PO_USUARIOS'
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    id_user = db.Column(db.Integer)
    nome = db.Column(db.String(255))
    email = db.Column(db.String(255))
    id_grupo = db.Column(db.Integer)
    grupo = db.Column(db.String(255))