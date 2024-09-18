from app import db

class VwPerfisSap(db.Model):
    __tablename__ = 'VW_PERFIS_SAP'

    Perfil = db.Column(db.String(255), primary_key=True, nullable=False)