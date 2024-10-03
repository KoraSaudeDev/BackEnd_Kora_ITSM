from app import db

class VwWFPOMateriais(db.Model):
    __tablename__ = 'VW_WF_PO_MATERIAIS'
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    referencia_id = db.Column(db.Integer)
    codigo = db.Column(db.String(40))
    grupo = db.Column(db.String(100))
    material = db.Column(db.String(255))
    qtd = db.Column(db.Integer)
    preco = db.Column(db.Numeric(20, 2))
    total = db.Column(db.Numeric(20, 2))
    id_status = db.Column(db.Integer)
    status = db.Column(db.String(255))
    motivo_reprova = db.Column(db.Text)
    cnpj_fornecedor = db.Column(db.String(40))
