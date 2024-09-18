from app import db

class TbCentroCusto(db.Model):
    __tablename__ = 'tb_centro_custo'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    centro_custo = db.Column(db.String(255), nullable=True)
    cod_empresa_sap = db.Column(db.Integer, nullable=True)
    nome_empresa = db.Column(db.String(200), nullable=True)
    cnpj = db.Column(db.String(40), nullable=True)
    cidade = db.Column(db.String(100), nullable=True)
    departamento = db.Column(db.String(200), nullable=True)
    descricao = db.Column(db.String(200), nullable=True)