from app import db

class TbWFPOAprovacoes(db.Model):
    __tablename__ = 'tb_wf_po_aprovacoes'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    referencia_id = db.Column(db.Integer, nullable=True)
    codigo = db.Column(db.String(40), nullable=True)
    grupo = db.Column(db.String(100), nullable=True)
    material = db.Column(db.String(255), nullable=True)
    qtd = db.Column(db.Integer, nullable=True)
    preco = db.Column(db.Numeric(20, 2), nullable=True)
    total = db.Column(db.Numeric(20, 2), nullable=True)
    status = db.Column(db.Integer, default=1, nullable=True)
    executor = db.Column(db.Integer, nullable=True)
    nome_executor = db.Column(db.String(255), nullable=True)
    motivo_reprova = db.Column(db.Text, nullable=True)