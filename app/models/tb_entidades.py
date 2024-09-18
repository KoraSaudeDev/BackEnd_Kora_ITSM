from app import db

class TbEntidades(db.Model):
    __tablename__ = 'tb_entidades'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sigla = db.Column(db.String(150), nullable=True)
    estado = db.Column(db.String(5), nullable=True)
    categoria = db.Column(db.String(25), nullable=True)