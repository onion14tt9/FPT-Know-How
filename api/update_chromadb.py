from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import openai
from dotenv import load_dotenv
import nltk
import chromadb
from chromadb.config import Settings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
import uuid

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust to your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load environment variables
load_dotenv()

# Set up OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

# ChromaDB client setup with authentication
client = chromadb.HttpClient(
    host='toiyeumeviet.hxann.com',
    port=80,
    settings=Settings(
        chroma_client_auth_provider="chromadb.auth.token_authn.TokenAuthClientProvider",
        chroma_server_authn_provider="chromadb.auth.simple_rbac_authz.SimpleRBACAuthorizationProvider",
        chroma_client_auth_credentials="hackathon-token"
    )
)

# Get or create collection
collection = client.get_or_create_collection(name='my_collection')


# Define input data model for API
class DocumentInput(BaseModel):
    file_name: str
    documents: list[str]


# Download NLTK data for text processing if not present
try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')


# Function to split text into manageable chunks
def split_text(documents: list[str]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=500,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents([Document(page_content=doc) for doc in documents])
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")
    return chunks


# Function to add chunks to ChromaDB collection
def save_to_chroma(chunks: list[Document], file_name: str):
    try:
        embedding_function = OpenAIEmbeddings()
        chunk_texts = [chunk.page_content for chunk in chunks]

        # Generate chunk IDs using the format "filename_guidid"
        chunk_ids = [f"{file_name}_{uuid.uuid4()}" for _ in range(len(chunks))]

        # Add metadata for each chunk
        metadata_list = [{"source": f"{file_name}"} for _ in range(len(chunks))]

        # Embed and add chunks to the Chroma collection
        print("Embedding documents...")
        embeddings_list = embedding_function.embed_documents(chunk_texts)
        print("Adding documents to ChromaDB...")
        collection.add(documents=chunk_texts, ids=chunk_ids, embeddings=embeddings_list, metadatas=metadata_list)
        print(f"Saved {len(chunks)} chunks to ChromaDB.")
    except Exception as e:
        print(f"Error saving to ChromaDB: {e}")


# FastAPI endpoint to add documents to ChromaDB
@app.post("/add_documents")
async def add_documents(input_data: DocumentInput):
    try:
        file_name = input_data.file_name
        print(f"Processing documents for file: {file_name}")
        
        # Split and embed provided documents
        chunks = split_text(input_data.documents)
        print("Document splitting completed.")
        
        # Save chunks to ChromaDB with formatted chunk IDs
        save_to_chroma(chunks, file_name)
        print("Documents added to ChromaDB successfully.")
        
        return {"message": "Documents added to ChromaDB successfully"}
    except Exception as e:
        print(f"Error in API document addition: {e}")
        raise HTTPException(status_code=500, detail=str(e))
