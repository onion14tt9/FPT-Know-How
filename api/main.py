from fastapi import FastAPI
from update_chromadb import app as update_chromadb_app
from query_data import app as query_data_app

# Create the main FastAPI app
app = FastAPI()

# Mount the apps at the appropriate paths
app.mount("/api/update", update_chromadb_app)
app.mount("/api/query_data", query_data_app) 

