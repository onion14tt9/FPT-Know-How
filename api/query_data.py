from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import chromadb
from chromadb.config import Settings
from chromadb.api.types import EmbeddingFunction
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import logging

# Define the custom embedding function
class CustomOpenAIEmbeddingFunction(EmbeddingFunction):
    def __init__(self, model_name='text-embedding-ada-002'):
        self.embedding_model = OpenAIEmbeddings(model=model_name)

    def __call__(self, input):
        if isinstance(input, str):
            input = [input]
        return self.embedding_model.embed_documents(input)

# Initialize FastAPI app
app = FastAPI()

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

# Set up embedding function and logging
embedding_function = CustomOpenAIEmbeddingFunction(model_name='text-embedding-ada-002')
logging.basicConfig(level=logging.INFO)

# Access the existing collection with the embedding function
collection = client.get_or_create_collection(
    name='my_collection',
    embedding_function=embedding_function
)

# Define the prompt template
PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

class QueryRequest(BaseModel):
    query_text: str

@app.post("/query")
async def query(request: QueryRequest):
    query_text = request.query_text

    if not query_text:
        raise HTTPException(status_code=400, detail="query_text is required")

    # Perform a similarity search in the ChromaDB collection
    results = collection.query(query_texts=[query_text], n_results=3)
    logging.info("Search results: %s", results)

    if len(results['documents']) == 0:
        return {"message": "Unable to find matching results."}

    # Prepare the context text for the prompt
    context_text_list = results['documents'][0]
    logging.info("Context text for prompt: %s", context_text_list)

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context='\n'.join(context_text_list), question=query_text)

    # Get response from the model
    model = ChatOpenAI()
    response_text = model.predict(prompt)
    logging.info("Model response: %s", response_text)

    # Extract sources (if available) from the results metadata
    sources = [meta.get("source", None) for meta in results['metadatas'][0]]
    formatted_response = {
        "response": response_text,
        "context_text": context_text_list,
        "sources": sources
    }

    return formatted_response
