from app import db

class VwAreasNegocio(db.Model):
    __tablename__ = 'VW_AREAS_NEGOCIO'

    Area_negocio = db.Column(db.String(255), nullable=True)
    Codigo = db.Column(db.Integer, primary_key=True, autoincrement=True)