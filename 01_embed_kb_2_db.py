import mariadb
from openai import OpenAI
import json
import os
import re
import pandas as pd
conn = mariadb.connect(
       host="127.0.0.1",
       port=3306,
       user="root",
       password="Password123!"
   )
cur = conn.cursor()
cur.execute("USE kb_content")
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY_KB_UNI'))
kb_input_file = "kb-crawler/crawler/output_250416.jsonl"

def read_kb_from_file(filename):
 with open(filename, "r") as file:
   return [json.loads(line) for line in file]

# Simply cut the content at max_chars and return one chunk
def chunkify(content, max_chars=2000):
    truncated_content = content[:max_chars]
    return [{'content': truncated_content}]

def embed(text):
    response = client.embeddings.create(
        input = text,
        model = "text-embedding-3-small" # max 8192 tokens (roughly 32k chars)
    )
    return response.data[0].embedding

def insert_kb_into_db(kb_input_file, limit=None):
   kb_pages = read_kb_from_file(kb_input_file)
   print(f"Total pages in {kb_input_file}: {len(kb_pages)}")
   for p_idx, p in enumerate(kb_pages[:limit]):
       kb_content = p["title"]+"\n"+p["content"]
       chunks = chunkify(kb_content)
       for chunk_idx, chunk in enumerate(chunks):
            # Check if record exists
            cur.execute("SELECT id FROM kb_chunks WHERE title = %s AND url = %s", (p["title"], p["url"]))
            existing_record = cur.fetchone()
            if existing_record:
                print(f"{p_idx}:{chunk_idx} - Skipping existing record '{p['title']}'")
                continue

            # if does not exist, embed and insert
            print(f"{p_idx}:{chunk_idx} - Embedding chunk (length {len(chunk['content'])}) from '{p['title']}'")
            embedding = embed(chunk["content"])
            cur.execute("""INSERT INTO kb_chunks (title, url, content, embedding)
                        VALUES (%s, %s, %s, VEC_FromText(%s))
                        ON DUPLICATE KEY UPDATE
                        content = VALUES(content),
                        embedding = VALUES(embedding)""",
                    (p["title"], p["url"], chunk["content"], str(embedding)))
       conn.commit()

insert_kb_into_db(kb_input_file, limit=None)
