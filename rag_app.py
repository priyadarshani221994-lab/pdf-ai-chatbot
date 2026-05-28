from fastapi import FastAPI
import chromadb
from sentence_transformers import SentenceTransformer

app = FastAPI()

model = SentenceTransformer('all-MiniLM-L6-v2')

client = chromadb.Client()

collection = client.create_collection("company_docs")

documents = ["Employees are allowed 12 casual leaves per year.", 
             
    "Work from home is allowed twice a week.", 

    "Office timing is 10 AM to 7PM."

    "Employees receive medical insurance benefits.",

    "Emlpyees must complete tasks before deadlines.",

    "Performance bonus is given yearly.",

    "Remote work is allowed for emergency  situations.",

    "Employees should inform manager before leave."

    ]

embeddings = model.encode(documents).tolist()

collection.add(
    documents=documents,
    embeddings=embeddings,
    ids=["1", "2", "3", "4", "5", "6", "7"]
)

@app.get("/ask")
def ask_question(query: str):

    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding, n_results=1
    )
    return {
        "query": query,
        "response":
results["documents"] [0]        
    }