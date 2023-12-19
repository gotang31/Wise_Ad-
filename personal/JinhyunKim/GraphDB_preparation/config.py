# config.py

#필요한 라이브러리 모음
from graphdatascience import GraphDataScience
import psycopg2 as pg

def get_gds():
    # neo4j graph DB에 따라서 설정을 바꿔주시면 됩니다.
    DB_URI = 'bolt://localhost:7687'
    DB_USER = 'neo4j'
    DB_PASSWORD = 'youreco09'

    # Python용 driver 생성
    gds = GraphDataScience(DB_URI, auth=(DB_USER, DB_PASSWORD))
    return gds

def get_conn():
    # postgresql에 따라서 설정을 바꿔주시면 됩니다.
    host = "127.0.0.1"
    dbname = "youreco"
    user = "postgres"
    password = "postgres"
    port = 5432
    
    # postgresql db 연결
    conn = pg.connect(host=host, dbname=dbname, user=user, password=password, port=port)
    return conn
