from app import db

class TbUsersNew(db.Model):
    __tablename__ = 'tb_users_new'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ds_nome = db.Column(db.String(255), nullable=False)
    nu_telefone = db.Column(db.String(20), nullable=True)
    ds_email = db.Column(db.String(150), nullable=True)
    nu_cpf = db.Column(db.String(20), nullable=True)
    nu_matricula = db.Column(db.Integer, nullable=True)
    ds_centro_custo = db.Column(db.String(80), nullable=True)
    ds_hub = db.Column(db.String(50), nullable=True)
    ds_unidade = db.Column(db.String(800), nullable=True)
    ds_area_negocio = db.Column(db.String(150), nullable=True)
    id_grupo = db.Column(db.Integer, nullable=True)
    id_papel = db.Column(db.Integer, nullable=True)
    id_papel_ticket = db.Column(db.Integer, nullable=True)
    dt_nascimento = db.Column(db.Date, nullable=True)
    bl_access = db.Column(db.Boolean, nullable=True)
    ds_cargo = db.Column(db.String(50), nullable=True)
    ds_funcao = db.Column(db.String(50), nullable=True)
    ds_nome_superior = db.Column(db.String(255), nullable=True)
    ds_email_superior = db.Column(db.String(255), nullable=True)
    bl_prestador_servico = db.Column(db.Integer, nullable=True)
    ds_tamanho_camiseta = db.Column(db.String(5), nullable=True)
    ds_tamanho_calcado = db.Column(db.String(5), nullable=True)
    bl_analista = db.Column(db.Integer, nullable=True)
    bl_fila = db.Column(db.Integer, nullable=True)