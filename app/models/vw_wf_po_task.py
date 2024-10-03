from app import db

class VwWFPOTasks(db.Model):
    __tablename__ = 'VW_WF_PO_TASKS'
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    referencia_id = db.Column(db.Integer)
    id_fase = db.Column(db.Integer)
    fase = db.Column(db.String(255))
    id_executor = db.Column(db.Integer)
    executor = db.Column(db.String(255))
    nome_executor = db.Column(db.String(255))
    numero_bloco = db.Column(db.String(15))
    inicio = db.Column(db.DateTime)
    fim = db.Column(db.DateTime)
    motivo_reprova = db.Column(db.Text)