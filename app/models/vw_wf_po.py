from app import db

class VwWFPO(db.Model):
    __tablename__ = 'VW_WF_PO'
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    dt_abertura = db.Column(db.DateTime)
    id_executor = db.Column(db.Integer)
    executor = db.Column(db.String(100))
    email = db.Column(db.String(100))
    nome = db.Column(db.String(100))
    area = db.Column(db.String(100))
    hub = db.Column(db.String(15))
    unidade = db.Column(db.String(100))
    centro_custo = db.Column(db.String(100))
    numero_bloco = db.Column(db.String(15))
    id_fase = db.Column(db.Integer)
    fase = db.Column(db.String(100))
    tipo_solicitacao = db.Column(db.String(50))
    grupo_material = db.Column(db.String(100))
    total_materiais = db.Column(db.Numeric(20, 2))
    descricao = db.Column(db.Text)
    observacoes = db.Column(db.Text)
    motivo_solicitacao = db.Column(db.String(100))
    id_bionexo = db.Column(db.Integer)
    crtl_bionexo = db.Column(db.Integer)
    id_sap = db.Column(db.String(20))
    dt_remessa = db.Column(db.DateTime)
    cod_fornecedor = db.Column(db.String(50))
    fornecedor = db.Column(db.String(100))
    dt_inicio_serv = db.Column(db.DateTime)
    dt_fim_serv = db.Column(db.DateTime)