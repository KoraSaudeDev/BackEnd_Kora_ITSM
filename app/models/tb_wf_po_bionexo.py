from app import db

class TbWFPOBionexo(db.Model):
    __tablename__ = 'tb_wf_po_bionexo'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    referencia_id = db.Column(db.Integer, nullable=True)
    cnpj = db.Column(db.String(40), nullable=True)
    razao_social = db.Column(db.String(255), nullable=True)
    faturamento_min = db.Column(db.Numeric(12, 2), nullable=True)
    prazo_entrega = db.Column(db.Integer, nullable=True)
    validade_proposta = db.Column(db.Date, nullable=True)
    id_forma_pag = db.Column(db.Integer, nullable=True)
    frete = db.Column(db.String(100), nullable=True)
    observacao = db.Column(db.Text, nullable=True)
    cod_produto = db.Column(db.String(40), nullable=True)
    quantidade = db.Column(db.Integer, nullable=True)
    fabricante = db.Column(db.String(255), nullable=True)
    embalagem = db.Column(db.String(255), nullable=True)
    preco_unitario = db.Column(db.Numeric(12, 2), nullable=True)
    preco_total = db.Column(db.Numeric(12, 2), nullable=True)
    comentario = db.Column(db.Text, nullable=True)
    inserido_em = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=True)