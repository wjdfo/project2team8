import pg8000
from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy
from transformers import AutoModel, AutoTokenizer
import json

def get_KoSimCSE(): #문장 임베딩 모듈 가져오는 함수
    model = AutoModel.from_pretrained('BM-K/KoSimCSE-roberta-multitask')
    tokenizer = AutoTokenizer.from_pretrained('BM-K/KoSimCSE-roberta-multitask')

    return model, tokenizer

model, tokenizer = get_KoSimCSE()

instance_connection_name = "your sql connection name" # @param {type:"string"}
db_user = "postgres" # @param {type:"string"}
db_pass = "your db password" # @param {type:"string"}
db_name = "your db name" # @param {type:"string"}

# initialize Cloud SQL Python Connector object
connector = Connector()

# DB 연결 함수
def getconn() -> pg8000.dbapi.Connection:
    conn: pg8000.dbapi.Connection = connector.connect(
        instance_connection_name,
        "pg8000",
        user=db_user,
        password=db_pass,
        db=db_name,
        ip_type=IPTypes.PUBLIC,
    )
    return conn

pool = sqlalchemy.create_engine(
    "postgresql+pg8000://",
    creator=getconn,
)

with pool.connect() as db_conn:
    db_conn.execute(
        sqlalchemy.text(
            "CREATE EXTENSION IF NOT EXISTS vector with schema public"
        )
    )
    db_conn.commit()

# pool.connect()하고 한 transaction만 수행 가능함.
# transaction 하나 수행하고 commit, close 하고 다시 connect 하기


with pool.connect() as db_conn:
    db_conn.execute(
        sqlalchemy.text(
            "CREATE EXTENSION IF NOT EXISTS pg_trgm with schema public"
        )
    )
    db_conn.commit()

#drop table
with pool.connect() as db_conn:
    try :
        db_conn.execute(
            sqlalchemy.text("drop table PROFNLEC")
        )
        db_conn.commit()
    except :
        print("table \'PROFNLEC\' does not exist.")

#create table
with pool.connect() as db_conn:
    db_conn.execute(
        sqlalchemy.text(
            """
            CREATE TABLE PROFNLEC(
                info varchar(50),
                info_num int,
                rating float,
                assignment varchar(50),
                team varchar(50),
                grade varchar(50),
                attendance varchar(50),
                test varchar(20),
                origin_text varchar(4096),
                v vector(768),
                PRIMARY KEY(info, info_num)
            )
            """
        )
    )
    db_conn.commit()
    print("table \'PROFNLEC\' created.")

#insert tuple
with pool.connect() as db_conn:
    rep = "original sentence"
    inputs = tokenizer(rep, padding = True, truncation = True, return_tensors = "pt")

    embeddings, _ = model(**inputs, return_dict = False)
    embedding_arr = embeddings[0][0].detach().numpy()
    embedding_str = ",".join(str(x) for x in embedding_arr)
    embedding_str = "["+embedding_str+"]"

    insert_stmt = sqlalchemy.text(
        "INSERT INTO PROFNLEC VALUES (:info, :info_num, :rating, :assignment, :team, :grade, :attendance, :test, :origin_text, :v)"
    )

    db_conn.execute(
        insert_stmt, parameters={"info": key,"info_num": i, "rating": rating, "assignment": assignment, "team":team,
                                "grade": grade, "attendance": attendance, "test": test,
                                "origin_text": rep, 'v': embedding_str}
    )

    db_conn.commit()
db_conn.close()