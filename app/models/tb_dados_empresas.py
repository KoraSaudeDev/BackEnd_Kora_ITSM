from app import db

class TbDadosEmpresas(db.Model):
    __tablename__ = 'tb_dados_empresas'

    codigo_empresa = db.Column(db.String(5), primary_key=True)
    acronimos = db.Column(db.String(50), nullable=True)
    nome_da_empresa = db.Column(db.String(255), nullable=True)
    user_principal_name_rede_email = db.Column(db.String(255), nullable=True)
    user_principal_name_rede = db.Column(db.String(255), nullable=True)
    script_path = db.Column(db.String(255), nullable=True)
    empresa = db.Column(db.String(255), nullable=True)
    cidade = db.Column(db.String(100), nullable=True)
    estado = db.Column(db.String(100), nullable=True)
    cep = db.Column(db.String(20), nullable=True)
    pais = db.Column(db.String(100), nullable=True)
    site = db.Column(db.String(255), nullable=True)
    endereco = db.Column(db.String(500), nullable=True)
    telefone = db.Column(db.String(20), nullable=True)