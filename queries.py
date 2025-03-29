query_uuid1_alarm_embeddings = """
SELECT source_uri, embedding, embedding_sparse
FROM v9__chatbot_documents
WHERE source_uri like '%58548175-ccef-4d6a-987c-f597b7d4d225%' OR source_uri like '%me_c_mk2%'
"""

query_uuid1_embedding_text = """
SELECT source_uri, embedding_text
FROM v9__chatbot_documents
WHERE source_uri like '%58548175-ccef-4d6a-987c-f597b7d4d225%' OR source_uri like '%me_c_mk2%'
"""





