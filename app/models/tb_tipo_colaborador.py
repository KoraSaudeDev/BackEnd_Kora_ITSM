from app import db

class TbTipoColaborador(db.Model):
    __tablename__ = 'tb_tipo_colaborador'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo = db.Column(db.String(255), nullable=True)
    bl_ativo = db.Column(db.Integer, default=1, nullable=False)