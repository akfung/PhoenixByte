from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer('multi-qa-mpnet-base-dot-v1')
embedding_model.save('/embedding_model/')
