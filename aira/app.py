import faiss
import numpy as np
import requests
import markdown
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import gradio as gr
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # Load variables from .env file

app = FastAPI()

# Load local documents from data/ directory
DOCS = [
    "../data/xAI_Service_Agreement_Revised.markdown",
    "../data/xAI_Invoice_Revised.markdown",
    "../data/xAI_Business_Proposal_Revised.markdown"
]

# Parse markdown documents
texts = []
for doc in DOCS:
    try:
        with open(doc, "r", encoding="utf-8") as f:
            md_content = f.read()
        html = markdown.markdown(md_content)
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text()
        texts.append({"content": text, "source": doc})
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail=f"Document {doc} not found")

# Initialize FAISS index
dimension = 1024  # nv-embedqa-e5-v5 dimension
index = faiss.IndexFlatL2(dimension)
embeddings = []

# Initialize NVIDIA API client with .env key
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
if not NVIDIA_API_KEY:
    raise HTTPException(status_code=500, detail="NVIDIA_API_KEY not set in .env")
client = OpenAI(
    api_key=NVIDIA_API_KEY,
    base_url="https://integrate.api.nvidia.com/v1"
)

def get_embedding(text, input_type="passage"):  # Default to "passage" for documents
    try:
        response = client.embeddings.create(
            input=[text],
            model="nvidia/nv-embedqa-e5-v5",
            encoding_format="float",
            extra_body={"input_type": input_type, "truncate": "END"}
        )
        return np.array(response.data[0].embedding, dtype=np.float32)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding API error: {str(e)}")

# Index documents
for doc in texts:
    embeddings.append(get_embedding(doc["content"]))
index.add(np.array(embeddings))

# Save FAISS index locally
faiss.write_index(index, "../data/faiss_index.bin")

# FastAPI endpoint for retrieval
class Query(BaseModel):
    text: str
    top_k: int = 3

@app.post("/retrieve")
async def retrieve(query: Query):
    try:
        query_embedding = get_embedding(query.text, input_type="query")
        distances, indices = index.search(np.array([query_embedding]), query.top_k)
        results = [texts[idx] for idx in indices[0]]
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retrieval error: {str(e)}")

# Placeholder for agent endpoint
@app.post("/agent")
async def agent(goal: Query):
    return {"steps": "TBD", "output": "TBD"}

# Gradio UI function
def run_agent(goal):
    if not goal.strip():
        return "Please enter a query."
    response = requests.post("http://localhost:8000/agent", json={"text": goal})
    result = response.json()
    return f"Steps: {result['steps']}\nOutput: {result['output']}"

# Mount Gradio UI to FastAPI
with gr.Blocks() as demo:
    gr.Markdown("# CRM Agent")
    query_input = gr.Textbox(label="Enter Query", placeholder="e.g., Summarize contract terms")
    output = gr.Textbox(label="Result", interactive=False, lines=5)
    gr.Button("Submit").click(
        fn=run_agent,
        inputs=query_input,
        outputs=output
    )

app = gr.mount_gradio_app(app, demo, path="/")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)