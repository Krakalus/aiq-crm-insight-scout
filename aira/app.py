import faiss
import numpy as np
import markdown
from bs4 import BeautifulSoup
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import gradio as gr
import os
from dotenv import load_dotenv

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

# NVIDIA API key (loaded from .env)
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
if not NVIDIA_API_KEY:
    raise HTTPException(status_code=500, detail="NVIDIA_API_KEY not set in .env")

def get_embedding(text):
    try:
        response = requests.post(
            "https://api.nvidia.com/nv-embedqa-e5-v5",
            headers={"Authorization": f"Bearer {NVIDIA_API_KEY}"},
            json={"text": text}
        )
        response.raise_for_status()
        return np.array(response.json()["embedding"], dtype=np.float32)
    except requests.RequestException as e:
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
        query_embedding = get_embedding(query.text)
        distances, indices = index.search(np.array([query_embedding]), query.top_k)
        results = [texts[idx] for idx in indices[0]]
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retrieval error: {str(e)}")

# Placeholder for agent endpoint (Step 8)
@app.post("/agent")
async def agent(goal: Query):
    return {"steps": "TBD", "output": "TBD"}

# Gradio UI
def run_agent(goal):
    response = requests.post("http://localhost:8000/agent", json={"text": goal})
    result = response.json()
    return result["steps"], result["output"]

with gr.Blocks() as demo:
    gr.Markdown("Agentic CRM Insight Scout")
    goal = gr.Textbox(label="Enter CRM Goal")
    steps = gr.Textbox(label="Agent Steps", interactive=False)
    output = gr.Textbox(label="Results", interactive=False)
    gr.Button("Run Agent").click(run_agent, inputs=goal, outputs=[steps, output])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)