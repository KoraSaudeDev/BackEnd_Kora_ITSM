from app import db

class VwHub(db.Model):
    __tablename__ = 'VW_HUB'
    
    HUB = db.Column(db.String(255), primary_key=True)