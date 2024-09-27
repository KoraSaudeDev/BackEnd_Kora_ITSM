from os import getenv
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = f"{getenv('DB_DRIVER')}://{getenv('DB_USERNAME')}:{quote_plus(getenv('DB_PASSWORD'))}@{getenv('DB_HOST')}/{getenv('DB_NAME')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    SAP_HANA_DATABASE_URI = f"hdb://{getenv('SAP_HANA_USERNAME')}:{quote_plus(getenv('SAP_HANA_PASSWORD'))}@{getenv('SAP_HANA_HOST')}:{getenv('SAP_HANA_PORT')}"
    
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = getenv('MAIL_USERNAME')
    MAIL_PASSWORD = getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = (getenv('MAIL_NAME'), getenv('MAIL_USERNAME'))