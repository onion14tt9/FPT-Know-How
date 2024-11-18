import chromadb
from chromadb.config import Settings

# Configure the ChromaDB client
client = chromadb.HttpClient(
    host='toiyeumeviet.hxann.com',
    port=80,
    settings=Settings(
        chroma_client_auth_provider="chromadb.auth.token_authn.TokenAuthClientProvider",
        chroma_server_authn_provider="chromadb.auth.simple_rbac_authz.SimpleRBACAuthorizationProvider",
        chroma_client_auth_credentials="hackathon-token"
    )
)

# Step 1: List all collections
collections = client.list_collections()
print("Collections in ChromaDB:")
for collection in collections:
    print(f"- {collection.name}")

# Step 2: Access a specific collection
collection_name = 'my_collection'

try:
    collection = client.get_collection(name=collection_name)
    print(f"\nAccessed collection '{collection_name}'.")
except Exception as e:
    print(f"Error accessing collection '{collection_name}': {e}")
    exit()

# Step 3: Retrieve and inspect data
try:
    # Removed 'ids' from the include list
    results = collection.get(include=['embeddings', 'documents', 'metadatas'])
    ids = results.get('ids', [])
    documents = results.get('documents', [])
    embeddings = results.get('embeddings', [])
    metadatas = results.get('metadatas', [])

    print(f"\nTotal items in '{collection_name}': {len(ids)}\n")

    for idx in range(len(ids)):
        print(f"Item {idx + 1}:")
        print(f"ID: {ids[idx]}")
        print(f"Document: {documents[idx]}")
        print(f"Metadata: {metadatas[idx]}")

        embedding = embeddings[idx]
        if embedding is not None:
            print(f"Embedding (first 5 values): {embedding[:5]}...\n")  # Print first 5 values for brevity
        else:
            print("Embedding: None\n")
except Exception as e:
    print(f"Error retrieving data from collection '{collection_name}': {e}")
