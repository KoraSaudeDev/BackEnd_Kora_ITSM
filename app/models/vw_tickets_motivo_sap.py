from app import db

class VwTicketsMotivoSap(db.Model):
    __tablename__ = 'VW_TICKETS_MOTIVO_SAP'

    ds_motivo = db.Column(db.String(255), primary_key=True, nullable=False)