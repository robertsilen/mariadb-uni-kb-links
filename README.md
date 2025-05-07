# mariadb-uni-kb-links

# Goal: linking MariaDB Uni with MariaDB KB
Wanted end result: code should suggest links between each "slide" within the [MariaDB for Uni material](https://github.com/mariadb/mariadb-for-universities) and articles in the [MariaDB Knowledgebase](https://mariadb.com/kb/en/) based on vector similarity.

# Example of end result
"Starting and Stopping the Server" from mariadb-dba-01-getting-started.md	could have a link to https://mariadb.com/kb/en/starting-and-stopping-mariadb-automatically/

# Steps in solution

With init.sql and instructions below:

1. Initialize MariaDB database and tables.

With 01_embed_kb_2_db.py:

2. Scrape MariaDB KB with [kb-crawler](https://github.com/cvicentiu/kb-crawler) to a jsonl file. 
3. Create a vector for each page (or the beginning of the page up to e.g. 2000 chars) with an embedding model. 
4. Insert each page into a  MariaDB table with fields: title, url, content, embedding

With 02_rag_search.py:

5. Iterate through MariaDB Uni material, and for each Uni "slide", create a vector with an embedding model. Search for closest KB vector, and document the 3 closest KB pages: title, url and vector distance.
6. Output in an xlsx for review and further consideration.

# Tech choices 

With python code, use [MariaDB Vector](https://mariadb.com/kb/en/vector-overview/) for vector storage and search with [MariaDB Python connector](https://pypi.org/project/mariadb/) on a [latest MariaDB Docker image](https://hub.docker.com/_/mariadb). 

For vectorization of text use embeddings models such as those on Huggingface's [embedding leaderboard](https://huggingface.co/spaces/mteb/leaderboard). Those especially good for semantic search are probably good for this solution.
1. Properietary API embedding models, e.g. 
- [OpenAI](https://platform.openai.com/docs/guides/embeddings) (used in this solution)
- [Anthropic](https://docs.anthropic.com/en/docs/build-with-claude/embeddings)
- [Mistral](https://docs.mistral.ai/capabilities/embeddings/)
2. or open models (see [definition](https://opensource.org/ai)), e.g.
- [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [BAAI/bge-large-en-v1.5](https://huggingface.co/BAAI/bge-large-en-v1.5)
- [intfloat/e5-large-v2](https://huggingface.co/intfloat/e5-large-v2)


# To initialize database

Pull and run the latest offical MariaDB image from Docker:
```
docker run -p 127.0.0.1:3306:3306  --name mdb -e MARIADB_ROOT_PASSWORD=Password123! -d mariadb:latest
```

Set up the database with:
```
docker exec -i mdb mariadb -uroot -pPassword123! < init.sql
```

To check that the docker image is running use ```docker ps```. To access the database: ```docker exec -it mdb mariadb -uroot -pPassword123!```.

x