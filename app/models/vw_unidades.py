from app import db

class VwUnidades(db.Model):
    __tablename__ = 'VW_UNIDADES'

    id = db.Column(db.Integer, primary_key=True)
    hub = db.Column(db.Integer, nullable=False)
    unidade_negocio = db.Column('Unidade de Negócio', db.String(255), nullable=False)
    sigla = db.Column('Sigla', db.String(50), nullable=False)
    cod_empresa = db.Column('Cod_Empresa', db.String(50), nullable=False)