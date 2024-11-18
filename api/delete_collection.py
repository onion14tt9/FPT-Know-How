import chromadb
from chromadb.config import Settings

def delete_collection():
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

    collection_name = "my_collection"

    try:
        # Attempt to retrieve the collection to ensure it exists
        collection = client.get_collection(name=collection_name)
        if collection:
            # Delete the collection
            client.delete_collection(name=collection_name)
            print(f"Collection '{collection_name}' has been successfully deleted.")
        else:
            print(f"Collection '{collection_name}' does not exist.")
    except FileNotFoundError:
        print(f"Collection '{collection_name}' not found.")
    except Exception as e:
        print(f"An error occurred while deleting the collection: {e}")

if __name__ == "__main__":
    delete_collection()
