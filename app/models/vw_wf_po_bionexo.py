from app import db

class VwWFPOBionexo(db.Model):
    __tablename__ = 'VW_WF_PO_BIONEXO'
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    referencia_id = db.Column(db.Integer)
    cnpj = db.Column(db.String(40))
    razao_social = db.Column(db.String(255))
    faturamento_min = db.Column(db.Numeric(20, 2))
    prazo_entrega = db.Column(db.Integer)
    validade_proposta = db.Column(db.DateTime)
    id_forma_pag = db.Column(db.Integer)
    frete = db.Column(db.String(255))
    observacao = db.Column(db.Text)
    cod_produto = db.Column(db.String(50))
    quantidade = db.Column(db.Integer)
    fabricante = db.Column(db.String(255))
    embalagem = db.Column(db.String(255))
    preco_unitario = db.Column(db.Numeric(20, 2))
    preco_total = db.Column(db.Numeric(20, 2))
    comentario = db.Column(db.Text)
    inserido_em = db.Column(db.DateTime)
