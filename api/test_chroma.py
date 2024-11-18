import chromadb
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings
from chromadb.config import Settings

# Connect with role-based authentication
client = chromadb.HttpClient(host='toiyeumeviet.hxann.com', port=80,
                             settings=Settings(
                                 chroma_client_auth_provider="chromadb.auth.token_authn.TokenAuthClientProvider",
                                 chroma_server_authn_provider="chromadb.auth.simple_rbac_authz.SimpleRBACAuthorizationProvider",
                                 chroma_client_auth_credentials="hackathon-token"
                             )
                             )

# Create or get a collection
collection = client.get_or_create_collection(name='my_collection')


# Define a custom embedding function (if needed)
class MyEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        # Implement your embedding logic here
        return [embedding for embedding in input]


# Insert a local document
documents = [
    "{\"No\": \"2\", \"Metric Name\": \"Effort Efficiency\", \"Formula\": \"EE = (Budgeted MM /(Calendar effort + paid Over-time effort))*100 - For On-Going project/Tentative project: + Budgeted MM: count from start date to current month + Calendar effort: count from start date to end date of current month - For Closed project/Cancelled project: + Budgeted MM : Total of project + Calendar effort: Total of project is count from start date to end date Note: 1. Budgeted MM: Effort is outsourced to FSU including Offshore, Near shore. These efforts are agreed between FSU/BU & AM for each order (source: CRM - quote/order) - PMs register the number of their projects' Budgeted effort on FI2.0, monthly separated 2. Calendar Effort is resource booked to implement projects = Σ Project team members * Actual duration of team members * % Effort allocated of team members Calendar effort by month is counted as above formula. With Duration is from start date to end date of month and converted rate of unit is Total working days in month equal to 1 MM. 3. Over time effort: HR confirmed by month\", \"Unit\": \"%\", \"Storage\": \"Post Mortem report\", \"Frequency\": \"Weekly/Milestone/Post-mortem/\"}"
]

ids = [
    "id13"
]
collection.add(documents=documents, ids=ids)

# Query the document
query_texts = ["What is the No of Metric name: Effort Efficiency?"]
results = collection.query(query_texts=query_texts, n_results=2)

# Print the results
print("Query Results:", results)
