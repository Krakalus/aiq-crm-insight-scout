# 🚀 AIQ CRM Insight Scout

## Revolutionize CRM with Agentic AI Precision

Welcome to **AIQ CRM Insight Scout**, a cutting-edge AI-powered CRM assistant crafted for a hackathon to master *Agentic AI* in Customer Relationship Management (CRM). This solution harnesses advanced AI to process legal and operational documents, enabling seamless **contract management**, **compliance**, and **customer support automation**. Born from a bold vision to innovate in the CRM industry, this project blends determination with innovation to deliver impactful results for hackathon success!

> [!NOTE]  
> First runs may take 15-20s to build the FAISS index. Subsequent queries average 13-15s, optimized for `top_k=3` document retrieval. Focus on the custom `(Time: X.Xs)` output for accurate timing.

## 📑 Table of Contents

- [Why AIQ CRM Insight Scout?](#why-aiq-crm-insight-scout)
- [Key Features](#key-features)
- [Motivation](#motivation)
- [Development Journey](#development-journey)
- [Installation](#installation)
- [Usage](#usage)
- [Example Queries](#example-queries)
- [Project Structure](#project-structure)
- [Flowchart Overview](#flowchart-overview)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Troubleshooting](#troubleshooting)
- [Future Improvements](#future-improvements)

## Why AIQ CRM Insight Scout?

- **Agentic AI Powerhouse**: Automates complex CRM tasks like contract analysis and compliance checks with a stateful LangGraph workflow.
- **CRM-Focused Innovation**: Tackles real-world challenges—managing *Data Processing Addendums*, *Terms of Service*, and regulatory compliance (e.g., CCPA, EAR).
- **Interactive Demo**: A sleek Gradio UI delivers fast, precise answers with processing time metrics, perfect for CRM teams.

## ✨ Key Features

- **📚 Robust Document Corpus**: Processes 9 markdown files (contracts, invoices, compliance checklists) simulating real CRM data.
- **🤖 Intelligent AI Agent**: Retrieves top 3 documents via FAISS, processes with NVIDIA’s *Llama-3.1-Nemotron-Nano-8B-v1*, and delivers intent-based answers or summaries.
- **🖥️ User-Friendly UI**: Gradio interface with clear *Answer*, *Plan*, and *Documents Retrieved* sections, including live processing time (e.g., `(Time: 14.3s)`).
- **⚖️ Compliance Ready**: Handles US regulations (*CCPA*, *EAR*, *FTC Act*) for precise legal and operational insights.
- **⚡ Optimized Performance**: Caches embeddings with `@lru_cache` and limits retrieval to `top_k=3` for fast, relevant responses.

## 🎯 Motivation

This project was born to:
- **Master Agentic AI**: Explore autonomous task handling for CRM automation.
- **Solve CRM Challenges**: Streamline legal document management and ensure compliance with laws like *CCPA* and *EAR*.
- **Impress at the Hackathon**: Build a demo showcasing practical AI integration, proving its value in the CRM industry.

## 🛠️ Development Journey

### Initial Setup
- **Backend**: FastAPI with LangGraph for stateful agent workflows (*plan*, *retrieve*, *output*).
- **AI Stack**: NVIDIA NIM API for embeddings (`nv-embedqa-e5-v5`) and LLM (`llama-3.1-nemotron-nano-8b-v1`) via OpenAI client.
- **Frontend**: Gradio UI for interactive query handling.
- **Retrieval**: FAISS for efficient document search.

### Challenges & Solutions
| Challenge | Solution |
|-----------|----------|
| **Embedding Generation** | Cached embeddings with `@lru_cache` and increased API timeout handling. |
| **Response Time (13-15s)** | Set `top_k=3` for focused retrieval; optimized FAISS indexing. |
| **Confusing Gradio UI** | Added custom `(Time: X.Xs)` to output; attempted `_js` override (failed due to TypeError). |
| **Document Management** | Expanded corpus to 9 files; removed stale `faiss_index.bin` for fresh indexing. |

## 💻 Installation

### Prerequisites
- **Python**: 3.8+
- **pip**: Python package manager
- **Hardware**: GPU recommended for NVIDIA NIM API (e.g., 1x H100 80GB or equivalent for local LLM inference).

### Setup Steps
1. **Clone the Repository**:
   ```bash
   git clone <your-repo-url>
   cd <repo-directory>
   ```

2. **Install Dependencies**:
   - Create a virtual environment (optional):
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate
     ```
   - Install packages:
     ```bash
     pip install -r requirements.txt
     ```
   - **Note**: If prompted to update pip (e.g., "A new release of pip is available: 25.1.1 -> 25.2"), run:
     ```bash
     python3 -m pip install --upgrade pip
     ```

3. **Configure Environment**:
   - Create a `.env` file in the root directory:
     ```
     NVIDIA_API_KEY=your_nvidia_api_key_here
     ```
   - Obtain your key from [NVIDIA API Catalog](https://integrate.api.nvidia.com/).

4. **Prepare Data**:
   - Ensure `../data/` contains these 9 markdown files:
     - `xAI_Service_Agreement_Revised.markdown`
     - `xAI_Invoice_Revised.markdown`
     - `xAI_Business_Proposal_Revised.markdown`
     - `Customer_Feedback_Survey.markdown`
     - `Performance_Report_Template.markdown`
     - `Project_Timeline.markdown`
     - `xAI_Data_Processing_Addendum.markdown`
     - `xAI_Terms_of_Service.markdown`
     - `xAI_Compliance_Checklist.markdown`

5. **Run the Application**:
   ```bash
   python app.py
   ```
   - Access the Gradio UI at [http://localhost:8000/](http://localhost:8000/).

## 🚀 Usage

### Interface
- **Enter Query**: Input a question (e.g., "What is the due date for the xAI invoice?") in the *Enter Query* textbox.
- **Submit**: Click the *Submit* button to process.
- **Output**:
  - **Answer**: Displays the response with processing time (e.g., "November 4, 2025 (Time: 14.3s)").
  - **Plan**: Shows the agent’s planning step.
  - **Documents Retrieved**: Indicates number of documents used (typically 3).

## 🔍 Example Queries

Test the AI’s versatility with these CRM-focused queries:

| Type | Query | Expected Output |
|------|-------|-----------------|
| Direct Answer | What is the timeline for xAI to notify Quantum Dynamics Inc. of a data breach under the DPA? | 72 hours per CCPA guidelines. |
| Summary | Summarize contract terms in the Terms of Service. | A concise overview of key terms (e.g., termination, confidentiality). |
| Compliance | What are the CCPA compliance requirements in the Compliance Checklist? | List of requirements: opt-out, record-keeping, impact assessments. |
| Financial | What is the total cost of the xAI invoice? | $38,000, including API subscription ($25,000), integration ($8,000), and training/support ($5,000). |
| Operational | What deliverables are expected in Phase 2 of the integration project? | Training completion report and pilot launch summary. |

## 📂 Project Structure

- `app.py`: Core script with FastAPI, LangGraph agent, and Gradio UI.
- `../data/`: Directory with 9 markdown files as the document corpus.
- `.env`: Stores NVIDIA API key.
- `requirements.txt`: Lists Python dependencies.

## 📊 Flowchart Overview

The following flowchart illustrates how **AIQ CRM Insight Scout** processes a user query to deliver CRM insights, from input to output:

<img src="images/CRM Insight Scout Flowchart.png" alt="AIQ CRM Insight Scout Flowchart">

- **User Inputs Query**: Starts with a CRM-specific query (e.g., "Summarize contract terms").
- **Display in Gradio UI**: Shows the interactive interface for input and results.
- **FastAPI Endpoint /agent**: Routes the query to the LangGraph agent.
- **LangGraph Agent**: Manages the workflow with *Plan*, *Retrieve*, and *Output* nodes.
- **LLM: Generate Plan**: Uses NVIDIA Llama-3.1 to create a retrieval strategy.
- **Retrieve Node**: Calls FastAPI `/retrieve` with FAISS vector search.
- **Embed Query**: Leverages NVIDIA Embedding API (`nv-embedqa-e5-v5`).
- **Search Index**: Queries the FAISS Index with preloaded CRM documents.
- **Return Top-K Docs**: Retrieves the top 3 relevant documents.
- **Output Node**: Generates the final answer or summary with NVIDIA Llama-3.1.
- **Return Output**: Displays the result (e.g., "Contract Summary") in the Gradio UI.

This visual breakdown highlights the Agentic AI workflow tailored for CRM efficiency. 

## 🤝 Contributing

This hackathon project welcomes contributions! Submit issues or pull requests via the [repository](<your-repo-url>). Let’s build the future of CRM AI together!

## 📜 License

Open-source for hackathon purposes unless otherwise specified. Review dependencies in `requirements.txt` for third-party licenses.

## 🙌 Acknowledgments

- **xAI**: Inspiration from Grok 3’s Agentic AI capabilities.
- **NVIDIA**: API access for embeddings and LLM inference.
- **Hackathon Organizers**: For providing a platform to innovate.
- **The Developer**: Fueled by relentless drive to master CRM AI!

## 🛠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| Document not found | Ensure all 9 markdown files are in `../data/`. |
| API Key Error | Verify `NVIDIA_API_KEY` in `.env` matches [NVIDIA API Catalog](https://integrate.api.nvidia.com/). |
| Timeout | Increase `timeout` in `requests.post` (line 196, `app.py`) or optimize network. |
| TypeError | Report errors with logs to the repository for support. |

## 🔮 Future Improvements

- **UI Enhancement**: Replace Gradio’s default progress bar with Server-Sent Events (SSE) for smoother feedback.
- **Performance**: Precompute embeddings for faster startup (under 10s).
- **Corpus Expansion**: Add more CRM documents (e.g., SLAs, audit logs) for broader use cases.
- **Compliance Depth**: Integrate more regulations (e.g., GDPR, HIPAA) for global CRM applicability.

*Built with 💪 by a passionate CRM innovator—Ready to transform the industry!*