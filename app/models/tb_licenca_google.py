from app import db

class TbLicencaGoogle(db.Model):
    __tablename__ = 'tb_licenca_google'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    licenca = db.Column(db.String(255), nullable=True)
    bl_ativo = db.Column(db.Integer, default=1, nullable=False)