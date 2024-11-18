import chromadb
from chromadb.config import Settings

def clear_chromadb_collection():
    """
    Clears all data from the specified ChromaDB collection without deleting the collection itself.
    """
    # Step 1: Configure the ChromaDB client
    try:
        client = chromadb.HttpClient(
            host='toiyeumeviet.hxann.com',
            port=80,
            settings=Settings(
                chroma_client_auth_provider="chromadb.auth.token_authn.TokenAuthClientProvider",
                chroma_server_authn_provider="chromadb.auth.simple_rbac_authz.SimpleRBACAuthorizationProvider",
                chroma_client_auth_credentials="hackathon-token"
            )
        )
        print("ChromaDB client initialized successfully.")
    except Exception as e:
        print(f"Failed to initialize ChromaDB client: {e}")
        return

    # Step 2: Access the specific collection
    collection_name = 'my_collection'
    try:
        collection = client.get_collection(name=collection_name)
        print(f"Accessed collection '{collection_name}'.")
    except Exception as e:
        print(f"Error accessing collection '{collection_name}': {e}")
        return

    # Step 3: Retrieve all item IDs in the collection
    try:
        results = collection.get()
        ids = results.get('ids', [])
        if not ids:
            print(f"No items found in collection '{collection_name}'. Nothing to delete.")
            return
        print(f"Found {len(ids)} item(s) in collection '{collection_name}'.")
    except Exception as e:
        print(f"Error retrieving items from collection '{collection_name}': {e}")
        return

    # Step 4: Delete all items by their IDs
    try:
        collection.delete(ids=ids)
        print(f"Successfully deleted {len(ids)} item(s) from collection '{collection_name}'.")
    except Exception as e:
        print(f"Error deleting items from collection '{collection_name}': {e}")

if __name__ == "__main__":
    clear_chromadb_collection()
