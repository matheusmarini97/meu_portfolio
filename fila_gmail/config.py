from urllib.parse import quote
import os

def connection_string():
    DB_PORT = os.getenv('DB_PORT')
    DB_USER = os.getenv('DB_USER')
    DB_HOST = os.getenv('DB_HOST')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_PASSWORD = quote(DB_PASSWORD)
    DB_SCHEMA = os.getenv('DB_SCHEMA')

    return f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_SCHEMA}\
        ?ssl_verify_cert=false'