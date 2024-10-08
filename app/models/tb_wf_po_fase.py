from app import db

class TbWFPOFase(db.Model):
    __tablename__ = 'tb_wf_po_fase'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = db.Column(db.String(255), nullable=True)
    n_bloco = db.Column(db.String(15), nullable=True)
    n_ordem = db.Column(db.Integer, nullable=True)
    id_grupo = db.Column(db.Integer, nullable=True)
    n_alcada_limit = db.Column(db.Integer, nullable=True)
    ds_tipo_compra = db.Column(db.String(50), nullable=True)
    ds_tipo_solic = db.Column(db.String(50), nullable=True)
    isIntegraBio = db.Column(db.Integer, nullable=True)
    isIntegraSAP = db.Column(db.Integer, nullable=True)