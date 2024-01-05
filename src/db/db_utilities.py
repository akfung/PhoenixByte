import psycopg2

from ..config import conn_s
from .schema import TableFactory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pgvector.psycopg2 import register_vector
from psycopg2 import sql
'''
Functions for bulk inserting embedded text into vector DB
'''

table_factory = TableFactory()

def insert_corpus(data:dict, model):
    '''Bulk insert of corpus data to the vector db'''
    engine = create_engine(conn_s) 
    SessionFactory = sessionmaker(bind=engine)
    session = SessionFactory()

    '''Insert cases'''
    for c in data['data']:

        summary = c['summary']
        for opinion in c['opinions']:
            print(opinion)
            table_name = opinion['justice']

            table = table_factory.get_table(table_name)
            if table is None:
                continue
            for written_opinion in opinion['written_opinion']:

                embedding = model.encode(written_opinion)
                new_row = table(
                    embedding=embedding,
                    opinion = written_opinion,
                    )

                session.add(new_row)
    session.commit()
    session.close()

def query_db(query:str, model, table:str='court_opinion', match_threshold:float=0.3, num_results:int=2) -> list:
    '''Query the vector db'''
    conn = psycopg2.connect(conn_s)
    register_vector(conn)
    cur = conn.cursor()
    # cur.execute('CREATE EXTENSION IF NOT EXISTS vector')
    cur.execute(sql.SQL(
        """SELECT opinion, 1 - (embedding <=> %(query_embedding)s) as similarity
        FROM {match_table} 
        WHERE 1 - (embedding <=> %(query_embedding)s) > %(match_threshold)s 
        ORDER BY similarity DESC LIMIT %(match_count)s""").format(match_table=sql.Identifier(table.lower())), 
        {"query_embedding": model.encode(query), 
         "match_threshold": match_threshold,
         "match_count":num_results})
    matches = cur.fetchall()
    return matches

def generate_index(table:str='documents', column_name:str='embedding'):
    '''Generate or reindex a table based on '''
    conn = psycopg2.connect(conn_s)
    cur = conn.cursor()
    cur.execute(f'create index on {table} using hnsw ({column_name} vector_l2_ops)')
    conn.close()
