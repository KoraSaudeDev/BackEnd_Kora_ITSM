from app import db

class TbAmbienteSap(db.Model):
    __tablename__ = 'tb_ambiente_sap'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ds_ambiente = db.Column(db.String(150), nullable=True)
    bl_ativo = db.Column(db.Integer, nullable=True)