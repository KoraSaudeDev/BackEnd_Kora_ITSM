from app import db

class VwUsuariosExecutores(db.Model):
    __tablename__ = 'VW_USUARIOS_EXECUTORES'
    
    grupo = db.Column(db.String(255))
    papel = db.Column(db.String(255))
    nome = db.Column(db.String(255))
    email = db.Column(db.String(255), primary_key=True)
    papel_nome = db.Column(db.Text, primary_key=True)