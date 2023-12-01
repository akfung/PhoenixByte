
-- Enable extension vector
create extension vector;

-- Create documents table to hold embeddings
CREATE TABLE IF NOT EXISTS documents (
  id SERIAL PRIMARY KEY,
  embedding vector(768),
  text text,
  created_at timestamptz DEFAULT now()
);

-- Create function for similarity search

create or replace function match_documents (
  query_embedding vector(1536),
  match_threshold float,
  match_count int
)
returns table (
  id bigint,
  content text,
  similarity float
)
language sql stable
as $$
  select
    documents.id,
    documents.text,
    1 - (documents.embedding <=> query_embedding) as similarity
  from documents
  where 1 - (documents.embedding <=> query_embedding) > match_threshold
  order by similarity desc
  limit match_count;
$$;

-- Instantiate HNSW indexes
-- create index on items using hnsw (column_name vector_l2_ops);
