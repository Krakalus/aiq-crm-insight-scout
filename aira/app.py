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
import logging
import time
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from typing import TypedDict, List
import httpx
import asyncio
from functools import lru_cache

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()  # Load variables from .env file

app = FastAPI()

# Load local documents from data/ directory
DOCS = [
    "../data/xAI_Service_Agreement_Revised.markdown",
    "../data/xAI_Invoice_Revised.markdown",
    "../data/xAI_Business_Proposal_Revised.markdown",
    "../data/Customer_Feedback_Survey.markdown",
    "../data/Performance_Report_Template.markdown",
    "../data/Project_Timeline.markdown",
    "../data/xAI_Data_Processing_Addendum.markdown",
    "../data/xAI_Terms_of_Service.markdown",
    "../data/xAI_Compliance_Checklist.markdown"
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

# Cache embeddings to avoid repeated API calls
@lru_cache(maxsize=100)
def get_embedding(text, input_type="passage"):
    try:
        logger.debug(f"Starting embedding for text: {text[:50]}...")
        client = OpenAI(
            api_key=os.getenv("NVIDIA_API_KEY"),
            base_url="https://integrate.api.nvidia.com/v1"
        )
        response = client.embeddings.create(
            input=[text],
            model="nvidia/nv-embedqa-e5-v5",
            encoding_format="float",
            extra_body={"input_type": input_type, "truncate": "END"},
            timeout=10
        )
        embedding = response.data[0].embedding
        logger.debug(f"Embedding completed for text: {text[:50]} with length {len(embedding)}")
        return np.array(embedding, dtype=np.float32)
    except Exception as e:
        logger.error(f"Embedding error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Embedding API error: {str(e)}")

# Initialize FAISS index
dimension = 1024
index = faiss.IndexFlatL2(dimension)
embeddings = [get_embedding(doc["content"]) for doc in texts]
index.add(np.array(embeddings))
faiss.write_index(index, "../data/faiss_index.bin")
logger.debug(f"FAISS index built with {index.ntotal} vectors")

# FastAPI endpoint for retrieval
class Query(BaseModel):
    text: str
    top_k: int = 3

@app.post("/retrieve")
async def retrieve(query: Query):
    try:
        logger.debug(f"Processing query: {query.text}")
        query_embedding = get_embedding(query.text, input_type="query")
        distances, indices = index.search(np.array([query_embedding]), query.top_k)
        results = [texts[idx] for idx in indices[0]]
        return {"results": results}
    except Exception as e:
        logger.error(f"Retrieval error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Retrieval error: {str(e)}")

# Define state for LangGraph agent
class AgentState(TypedDict):
    goal: str
    plan: str
    results: List[dict]
    output: str

# Tool for retrieval with async HTTP call
@tool
async def retrieve_tool(plan: str):
    """Retrieve relevant CRM documents based on plan."""
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:8000/retrieve", json={"text": plan, "top_k": 3}, timeout=20.0)
        response.raise_for_status()
        return response.json()["results"]

# Initialize LLM with NVIDIA NIM
llm = ChatOpenAI(
    model="nvidia/llama-3.1-nemotron-nano-8b-v1",
    api_key=os.getenv("NVIDIA_API_KEY"),
    base_url="https://integrate.api.nvidia.com/v1"
)

# Build LangGraph with async nodes
async def entry_node(state):
    plan = await llm.ainvoke(f"Plan briefly for CRM goal: {state['goal']}")
    return {"plan": plan.content if hasattr(plan, 'content') else str(plan)}

async def retrieve_node(state):
    results = await retrieve_tool.ainvoke(state['plan'])
    return {"results": results}

async def output_node(state):
    # Check if the query explicitly requests summarization
    is_summary_request = any(keyword in state['goal'].lower() for keyword in ["summarize", "summary", "overview"])
    
    if is_summary_request:
        # Summarize when explicitly requested
        output = await llm.ainvoke(
            f"Provide a brief summary for the goal '{state['goal']}': {state['results']}"
        )
    else:
        # Provide direct, concise answer for specific queries
        output = await llm.ainvoke(
            f"Answer the query '{state['goal']}' directly and concisely using the following information: {state['results']}. "
            f"Do not summarize unless explicitly requested. Focus on the specific details asked in the query."
        )
    return {"output": output.content if hasattr(output, 'content') else str(output)}

graph = StateGraph(AgentState)
graph.add_node("entry", entry_node)
graph.add_node("retrieve", retrieve_node)
graph.add_node("output", output_node)
graph.set_entry_point("entry")
graph.add_edge("entry", "retrieve")
graph.add_edge("retrieve", "output")
graph.add_edge("output", END)
agent = graph.compile()

# Agent endpoint with LangGraph
@app.post("/agent")
async def process_agent(goal: Query):
    try:
        logger.debug(f"Processing goal: {goal.text}")
        state = {"goal": goal.text}
        result = await agent.ainvoke(state)
        steps = [
            f"Plan: {result['plan']}",
            f"Retrieved: {len(result.get('results', []))} documents",
            f"Output: {result['output']}"
        ]
        return {"steps": "\n".join(steps), "output": result["output"]}
    except Exception as e:
        logger.error(f"Agent error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")

# Gradio UI function
def run_agent(goal):
    if not goal.strip():
        return "Please enter a query.", "", ""
    start_time = time.time()
    response = requests.post("http://localhost:8000/agent", json={"text": goal}, timeout=60)
    processing_time = time.time() - start_time
    if response.status_code == 500:
        return f"Error: Agent failed to process the query. (Time: {processing_time:.1f}s)", "", ""
    result = response.json()
    steps = result["steps"].split("\n")
    plan = next((s.split(": ")[1] for s in steps if s.startswith("Plan:")), "No plan available.")
    retrieved = next((s.split(": ")[1] for s in steps if s.startswith("Retrieved:")), "No documents retrieved.")
    output = result["output"]
    return f"{output} (Time: {processing_time:.1f}s)"

# Mount Gradio UI to FastAPI
with gr.Blocks() as demo:
    gr.Markdown("# CRM Agent")
    query_input = gr.Textbox(label="Enter Query", placeholder="e.g., Summarize contract terms")
    with gr.Row():
        output_result = gr.Textbox(label="Answer", interactive=False, lines=5)
    gr.Button("Submit").click(
        fn=run_agent,
        inputs=query_input,
        outputs=[output_result]
    )

app = gr.mount_gradio_app(app, demo, path="/")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)