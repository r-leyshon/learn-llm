"""Create datastax Astradb vector store and execute similarity search.

1. Uses openai to provide embeddings. This costs approx 1 cent each time the
script is run.
2. Creates an Astradb vector store.
3. Converts an arrow table of philosophical quotes to langchain documents.
4. Stores those documents within the vector store.
5. Runs a similarity search against a custom quote.
"""
import os

from datasets import load_dataset
from langchain_astradb import AstraDBVectorStore
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from pyprojroot import here
import toml

secrets_pth = here(".secrets.toml")
secrets = toml.load(secrets_pth)

ASTRA_DB_APPLICATION_TOKEN = secrets["datastax"]["ASTRA_DB_APPLICATION_TOKEN"]
ASTRA_DB_API_ENDPOINT = secrets["datastax"]["ASTRA_DB_API_ENDPOINT"]
ASTRA_DB_KEYSPACE = secrets["datastax"]["ASTRA_DB_KEYSPACE"] # currently under
# dashboard > select db > Data Explorer > Namespace
OPENAI_API_KEY = secrets["openai"]["OPENAI_API_KEY"] 
CLIENT_ID = secrets["datastax"]["client-id"]

# Specify the embeddings model, database, and collection to use. If the
# collection does not exist, it is created automatically.
embedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
vstore = AstraDBVectorStore(
    embedding=embedding,
    namespace=ASTRA_DB_KEYSPACE,
    collection_name="test",
    token=ASTRA_DB_APPLICATION_TOKEN,
    api_endpoint=ASTRA_DB_API_ENDPOINT,
)

# Load a small dataset of philosophical quotes with the Python dataset module.

philo_dataset = load_dataset("datastax/philosopher-quotes")["train"]
print("An example entry:")
print(philo_dataset[16])

# Process metadata and convert to LangChain documents.
docs = []
for entry in philo_dataset:
    metadata = {"author": entry["author"]}
    if entry["tags"]:
        # Add metadata tags to the metadata dictionary
        for tag in entry["tags"].split(";"):
            metadata[tag] = "y"
    # Add a LangChain document with the quote and metadata tags
    doc = Document(page_content=entry["quote"], metadata=metadata)
    docs.append(doc)

# Compute embeddings for each document and store in the database.
inserted_ids = vstore.add_documents(docs)
print(f"\nInserted {len(inserted_ids)} documents.")

# Show quotes that are similar to a specific quote.
results = vstore.similarity_search("Our life is what we make of it", k=3)
for res in results:
    print(f"* {res.page_content} [{res.metadata}]")
