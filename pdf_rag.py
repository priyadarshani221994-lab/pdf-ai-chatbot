from fastapi import FastAPI
import chromadb
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader

app = FastAPI()

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.Client()

collection = client.create_collection("pdf_docs")

# Read PDF
reader = PdfReader("pdfs/resume.pdf")

text = ""

for page in reader.pages:
    text += page.extract_text()

documents = text.split(".")

documents = [doc.strip() for doc in documents if doc.strip()]

embeddings = model.encode(documents).tolist()

ids = [str(i) for i in range(len(documents))]

collection.add(
    documents=documents,
    embeddings=embeddings,
    ids=ids
)

@app.get("/ask")
def ask_question(query: str):

    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=2
    )

    return {
        "query": query,
        "response": results["documents"][0]
    }