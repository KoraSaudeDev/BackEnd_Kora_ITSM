from app import db

class VwItsmSubcategoria(db.Model):
    __tablename__ = 'VW_ITSM_SUBCATEGORIA'
    
    id_categoria = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(255))
    id_subcategoria = db.Column(db.Integer, primary_key=True)
    subcategoria = db.Column(db.String(255))