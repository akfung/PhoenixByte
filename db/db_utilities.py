import psycopg2
from sentence_transformers import SentenceTransformer
import numpy as np
import os

from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from psycopg2.extras import execute_values
from pgvector.psycopg2 import register_vector
from pgvector.sqlalchemy import Vector
'''
Functions for bulk inserting embedded text into vector DB
'''

model = SentenceTransformer('multi-qa-mpnet-base-dot-v1')

conn_s = "postgresql://{user}:{password}@{host}:{port}/{db_name}".format(
    user= os.environ['DB_USER'],
    password= os.environ['DB_PASSWORD'],
    host= os.environ['DB_HOST'], 
    port= os.environ['DB_PORT'], 
    db_name = os.environ['DB_NAME'],
)

class Documents(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True, autoincrement=True)
    embedding = Column(Vector)
    text = Column(String)
    created_at = Column(TIMESTAMP)

engine = create_engine(conn_s) 
SessionFactory = sessionmaker(bind=engine)
session = SessionFactory()

'''Insert cases'''
SessionFactory = sessionmaker(bind=engine)
session = SessionFactory()

for c in case_data['data']:
    print(c)
    embedding = model.encode(c['opinion'])

    new_row = Documents(
        embedding=embedding,
        text = c['opinion'],
        )

    session.add(new_row)

session.commit()

session.close()

