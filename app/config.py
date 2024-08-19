from os import getenv
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

password = quote_plus(getenv('DB_PASSWORD'))

class Config:
    SQLALCHEMY_DATABASE_URI = f"{getenv('DB_DRIVER')}://{getenv('DB_USERNAME')}:{password}@{getenv('DB_HOST')}/{getenv('DB_NAME')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
