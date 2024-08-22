from app import db

class VwItsmAssunto(db.Model):
    __tablename__ = 'VW_ITSM_ASSUNTO'
    
    id_categoria = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(255))
    id_subcategoria = db.Column(db.Integer, primary_key=True)
    subcategoria = db.Column(db.String(255))
    id_assunto = db.Column(db.Integer, primary_key=True)
    assunto = db.Column(db.String(255))
    prioridade = db.Column(db.String(255))
    sla = db.Column(db.Integer)
    tipo_assunto = db.Column(db.String(255))
    grupo_atendimento = db.Column(db.String(255))