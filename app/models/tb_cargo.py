from app import db

class TbCargo(db.Model):
    __tablename__ = 'tb_cargo'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cargo = db.Column(db.String(255), nullable=True)