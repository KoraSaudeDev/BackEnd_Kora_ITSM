from app import db

class VwAreasDiretoria(db.Model):
    __tablename__ = 'VW_AREAS_DIRETORIA'

    ds_area = db.Column(db.String(255), primary_key=True, nullable=False)