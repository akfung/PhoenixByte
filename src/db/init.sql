
-- Enable extension vector
create extension vector;

-- Create documents table to hold embeddings
CREATE TABLE IF NOT EXISTS court_opinion (
  id SERIAL PRIMARY KEY,
  embedding vector(768),
  opinion text,
  created_at timestamptz DEFAULT now()
);
CREATE TABLE IF NOT EXISTS alito (
  id SERIAL PRIMARY KEY,
  embedding vector(768),
  opinion text,
  created_at timestamptz DEFAULT now()
);
CREATE TABLE IF NOT EXISTS barrett (
  id SERIAL PRIMARY KEY,
  embedding vector(768),
  opinion text,
  created_at timestamptz DEFAULT now()
);
CREATE TABLE IF NOT EXISTS breyer (
  id SERIAL PRIMARY KEY,
  embedding vector(768),
  opinion text,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS ginsburg (
  id SERIAL PRIMARY KEY,
  embedding vector(768),
  opinion text,
  created_at timestamptz DEFAULT now()
);
CREATE TABLE IF NOT EXISTS gorsuch (
  id SERIAL PRIMARY KEY,
  embedding vector(768),
  opinion text,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS jackson (
  id SERIAL PRIMARY KEY,
  embedding vector(768),
  opinion text,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS kagan (
  id SERIAL PRIMARY KEY,
  embedding vector(768),
  opinion text,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS kavanaugh (
  id SERIAL PRIMARY KEY,
  embedding vector(768),
  opinion text,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS kennedy (
  id SERIAL PRIMARY KEY,
  embedding vector(768),
  opinion text,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS roberts (
  id SERIAL PRIMARY KEY,
  embedding vector(768),
  opinion text,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS scalia (
  id SERIAL PRIMARY KEY,
  embedding vector(768),
  opinion text,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS sotomayor (
  id SERIAL PRIMARY KEY,
  embedding vector(768),
  opinion text,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS thomas (
  id SERIAL PRIMARY KEY,
  embedding vector(768),
  opinion text,
  created_at timestamptz DEFAULT now()
);

-- Create function for similarity search

-- create or replace function match_documents (
--   query_embedding vector(768),
--   match_table text,
--   match_threshold float,
--   match_count int
-- )
-- returns table (
--   id bigint,
--   content text,
--   similarity float
-- )
-- language sql stable
-- as $$
--   select
--     match_table.id,
--     match_table.opinion,
--     1 - (match_table.embedding <=> query_embedding) as similarity
--   from match_table
--   where 1 - (match_table.embedding <=> query_embedding) > match_threshold
--   order by similarity desc
--   limit match_count;
-- $$;

-- Instantiate HNSW indexes
-- create index on items using hnsw (column_name vector_l2_ops);
