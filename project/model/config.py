# config.py
#필요한 라이브러리 모음
from graphdatascience import GraphDataScience
import psycopg2 as pg


def get_gds():
    # neo4j graph DB에 따라서 설정을 바꿔주시면 됩니다.
    DB_URI = 'bolt://localhost:7687'
    DB_USER = 'neo4j'
    DB_PASSWORD = 'inisw_test'
    # eno4j sandbox (온라인 DB)를 사용할 경우 위에 것을 comment하고 다음을 uncomment 해주세요.
    # 현재 작성되어 있는 neo4j sandbox는 12월 21일 까지 유효합니다.
    #DB_URI = 'bolt://18.212.191.71:7687'
    #DB_USER = 'neo4j'
    #DB_PASSWORD = 'burns-mints-shocks'	

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
