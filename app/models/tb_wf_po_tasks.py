from app import db

class TbWFPOTasks(db.Model):
    __tablename__ = 'tb_wf_po_tasks'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    referencia_id = db.Column(db.Integer, nullable=True)
    fase = db.Column(db.Integer, nullable=True)
    executor = db.Column(db.Integer, nullable=True)
    nome_executor = db.Column(db.String(255), nullable=True)
    numero_bloco = db.Column(db.String(15), nullable=True)
    inicio = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=True)
    fim = db.Column(db.DateTime, nullable=True)
    motivo_reprova = db.Column(db.Text, nullable=True)