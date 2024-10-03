from app import db

class TbSuporteMenu(db.Model):
    __tablename__ = 'tb_suporte_menu'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String(100), nullable=False)
    route = db.Column(db.String(255), nullable=True)
    icon = db.Column(db.String(50), nullable=True)
    parent_id = db.Column(db.Integer, nullable=True)
    ordem = db.Column(db.Integer, nullable=False, default=1)
    apiCounterConfig = db.Column(db.String(1000), nullable=True)
    componentPath = db.Column(db.String(255), nullable=True)
    active = db.Column(db.Boolean, default=True)
    parent_relation = db.Column(db.Integer)