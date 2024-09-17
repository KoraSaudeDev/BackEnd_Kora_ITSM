from os import getenv
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

password = quote_plus(getenv('DB_PASSWORD'))

class Config:
    SQLALCHEMY_DATABASE_URI = f"{getenv('DB_DRIVER')}://{getenv('DB_USERNAME')}:{password}@{getenv('DB_HOST')}/{getenv('DB_NAME')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = getenv('MAIL_USERNAME')
    MAIL_PASSWORD = getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = (getenv('MAIL_NAME'), getenv('MAIL_USERNAME'))