from app import db

class VwItsmStatusTickets(db.Model):
    __tablename__ = 'VW_ITSM_STATUS_TICKETS'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    bl_ativo = db.Column(db.Integer)