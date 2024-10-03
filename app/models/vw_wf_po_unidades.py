from app import db

class VwWFPOUnidades(db.Model):
    __tablename__ = 'VW_WF_PO_UNIDADES'

    unidade = db.Column(db.String(255), primary_key=True)
    nu_codigo_sap = db.Column(db.String(50))
    bloco_produto = db.Column(db.String(255))
    bloco_servico = db.Column(db.String(255))
    hub = db.Column(db.String(50))