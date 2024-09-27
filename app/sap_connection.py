from hdbcli import dbapi
from os import getenv

def ConnectionSAPHANA():
    try:
        connection = dbapi.connect(
            address=getenv('SAP_HANA_HOST'),
            port=int(getenv('SAP_HANA_PORT')),
            user=getenv('SAP_HANA_USERNAME'),
            password=getenv('SAP_HANA_PASSWORD')
        )
        return connection
    except dbapi.Error as e:
        print(f"Erro ao conectar ao SAP HANA: {e}")
        return None